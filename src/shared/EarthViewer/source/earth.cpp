/**
 * Orbital Visualization Platform - Earth Viewer
 * 
 * A high-fidelity OpenGL Earth renderer with satellite trajectory visualization.
 * Features:
 *   - NASA Blue Marble day texture with city lights (Black Marble) at night
 *   - Animated cloud layer with Perlin noise drift
 *   - Day/night cycle with smooth terminator
 *   - Satellite trajectory rendering from JSON data files
 *   - Interactive trackball camera controls
 * 
 * This viewer integrates with Python orbital mechanics simulations,
 * loading trajectory data exported from the Starlink Propagator and
 * other constellation design tools.
 */

// Prevent Windows min/max macros from conflicting with std::min/max
#define NOMINMAX

#include "common.h"
#include "SourcePath.h"
#include "common/lodepng.h"
#include <fstream>
#include <sstream>
#include <vector>
#include <cmath>
#include <algorithm>

using namespace Angel;

typedef vec4 color4;

// ============================================================================
// Satellite Data Structures
// ============================================================================

struct SatellitePosition {
    float x, y, z;      // Position in normalized Earth radii
    float r, g, b;      // Color
};

struct SatelliteTrajectory {
    std::string name;
    std::vector<SatellitePosition> positions;
    vec3 color;
    int current_frame;
};

std::vector<SatelliteTrajectory> satellites;
int global_frame = 0;
bool show_satellites = true;
bool show_trails = true;
int trail_length = 100;

// ============================================================================
// OpenGL State
// ============================================================================

// Lighting
vec4 light_position(0.0, 0.0, 10.0, 1.0);
vec4 ambient(0.0, 0.0, 0.0, 1.0);

// Earth mesh
Mesh* mesh;

// OpenGL handles
GLuint buffer;
GLuint vao;
GLuint ModelViewEarth, ModelViewLight, NormalMatrix, Projection;
bool wireframe;
GLuint program;

// Satellite rendering
GLuint sat_vao, sat_vbo;
GLuint sat_program;
GLuint sat_ModelView, sat_Projection, sat_Color;

// Trackball
Trackball tb;

// Textures
GLuint month_texture;
GLuint night_texture;
GLuint cloud_texture;
GLuint perlin_texture;

// Animation
float animate_time;
float rotation_angle;
bool paused = false;
float playback_speed = 1.0f;
bool auto_rotate = true;        // Earth auto-rotation
float earth_rotation = 0.0f;    // Current Earth rotation angle
float earth_rotation_speed = 0.08f;  // Degrees per frame (slower, more realistic)

// ============================================================================
// Texture Loading (Windows-compatible)
// ============================================================================

#ifdef _WIN32
static unsigned int lodepng_decode_wfopen(std::vector<unsigned char>& out, unsigned& w, unsigned& h,
    const std::string& filename, LodePNGColorType colortype = LCT_RGBA, unsigned bitdepth = 8) {
    std::wstring wcfn;
    if (u8names_towc(filename.c_str(), wcfn) != 0) return 78;
    FILE* fp = _wfopen(wcfn.c_str(), L"rb");
    if (fp == NULL) return 78;

    std::vector<unsigned char> buf;
    fseek(fp, 0L, SEEK_END);
    long const size = ftell(fp);
    if (size < 0) { fclose(fp); return 78; }

    fseek(fp, 0L, SEEK_SET);
    buf.resize(size);
    fread(buf.data(), 1, size, fp);
    fclose(fp);

    return lodepng::decode(out, w, h, buf, colortype, bitdepth);
}
#endif

void loadFreeImageTexture(const char* lpszPathName, GLuint textureID, GLuint GLtex) {
    std::vector<unsigned char> image;
    unsigned int width, height;

#ifdef _WIN32
    unsigned error = lodepng_decode_wfopen(image, width, height, lpszPathName, LCT_RGBA, 8);
#else
    unsigned error = lodepng::decode(image, width, height, lpszPathName, LCT_RGBA, 8);
#endif

    if (error) {
        std::cout << "Texture load error " << error << ": " << lodepng_error_text(error) << std::endl;
        return;
    }

    std::cout << "Loaded texture: " << width << "x" << height << std::endl;

    glActiveTexture(GLtex);
    glBindTexture(GL_TEXTURE_2D, textureID);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, &image[0]);
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glGenerateMipmap(GL_TEXTURE_2D);

    image.clear();
}

// ============================================================================
// Satellite Data Loading (Simple JSON-like format)
// ============================================================================

/**
 * Loads satellite trajectory data from a simple text format.
 * Format per line: name,x,y,z,r,g,b
 * Satellites are grouped by name.
 * 
 * In production, this would parse proper JSON using a library like nlohmann/json.
 * For simplicity, we use a CSV-like format that Python can easily export.
 */
bool loadTrajectoryData(const std::string& filepath) {
    std::ifstream file(filepath);
    if (!file.is_open()) {
        std::cout << "No trajectory file found at: " << filepath << std::endl;
        std::cout << "Running in Earth-only mode." << std::endl;
        return false;
    }

    std::string line;
    std::string current_name = "";
    SatelliteTrajectory* current_sat = nullptr;

    // Skip header
    std::getline(file, line);

    while (std::getline(file, line)) {
        std::stringstream ss(line);
        std::string name;
        float x, y, z, r, g, b;
        char comma;

        std::getline(ss, name, ',');
        ss >> x >> comma >> y >> comma >> z >> comma >> r >> comma >> g >> comma >> b;

        if (name != current_name) {
            // New satellite
            satellites.push_back(SatelliteTrajectory());
            current_sat = &satellites.back();
            current_sat->name = name;
            current_sat->color = vec3(r, g, b);
            current_sat->current_frame = 0;
            current_name = name;
        }

        if (current_sat) {
            SatellitePosition pos = { x, y, z, r, g, b };
            current_sat->positions.push_back(pos);
        }
    }

    std::cout << "Loaded " << satellites.size() << " satellite trajectories." << std::endl;
    return true;
}

// ============================================================================
// Input Callbacks
// ============================================================================

static void error_callback(int error, const char* description) {
    fprintf(stderr, "GLFW Error: %s\n", description);
}

static void key_callback(GLFWwindow* window, int key, int scancode, int action, int mods) {
    if (action != GLFW_PRESS) return;

    switch (key) {
        case GLFW_KEY_ESCAPE:
            glfwSetWindowShouldClose(window, GLFW_TRUE);
            break;
        case GLFW_KEY_SPACE:
            paused = !paused;
            std::cout << (paused ? "Paused" : "Playing") << std::endl;
            break;
        case GLFW_KEY_W:
            wireframe = !wireframe;
            break;
        case GLFW_KEY_S:
            show_satellites = !show_satellites;
            std::cout << "Satellites: " << (show_satellites ? "ON" : "OFF") << std::endl;
            break;
        case GLFW_KEY_T:
            show_trails = !show_trails;
            std::cout << "Trails: " << (show_trails ? "ON" : "OFF") << std::endl;
            break;
        case GLFW_KEY_A:
            auto_rotate = !auto_rotate;
            std::cout << "Auto-rotate: " << (auto_rotate ? "ON" : "OFF") << std::endl;
            break;
        case GLFW_KEY_UP:
            playback_speed *= 2.0f;
            if (playback_speed > 16.0f) playback_speed = 16.0f;
            std::cout << "Speed: " << playback_speed << "x" << std::endl;
            break;
        case GLFW_KEY_DOWN:
            playback_speed *= 0.5f;
            if (playback_speed < 0.125f) playback_speed = 0.125f;
            std::cout << "Speed: " << playback_speed << "x" << std::endl;
            break;
        case GLFW_KEY_LEFT:
            earth_rotation_speed *= 0.5f;
            std::cout << "Rotation speed: " << earth_rotation_speed << " deg/frame" << std::endl;
            break;
        case GLFW_KEY_RIGHT:
            earth_rotation_speed *= 2.0f;
            std::cout << "Rotation speed: " << earth_rotation_speed << " deg/frame" << std::endl;
            break;
        case GLFW_KEY_R:
            global_frame = 0;
            earth_rotation = 0.0f;
            std::cout << "Reset to frame 0" << std::endl;
            break;
        case GLFW_KEY_H:
            std::cout << "\n=== CONTROLS ===" << std::endl;
            std::cout << "Mouse drag    - Rotate view" << std::endl;
            std::cout << "Shift + drag  - Zoom" << std::endl;
            std::cout << "Alt + drag    - Pan" << std::endl;
            std::cout << "SPACE         - Pause/Play" << std::endl;
            std::cout << "A             - Toggle auto-rotate" << std::endl;
            std::cout << "S             - Toggle satellites" << std::endl;
            std::cout << "T             - Toggle trails" << std::endl;
            std::cout << "W             - Toggle wireframe" << std::endl;
            std::cout << "UP/DOWN       - Satellite speed" << std::endl;
            std::cout << "LEFT/RIGHT    - Earth rotation speed" << std::endl;
            std::cout << "R             - Reset" << std::endl;
            std::cout << "H             - Show this help" << std::endl;
            std::cout << "ESC           - Quit" << std::endl;
            std::cout << "================\n" << std::endl;
            break;
    }
}

static void mouse_click(GLFWwindow* window, int button, int action, int mods) {
    if (GLFW_RELEASE == action) {
        tb.moving = tb.scaling = tb.panning = false;
        return;
    }

    if (mods & GLFW_MOD_SHIFT) {
        tb.scaling = true;
    } else if (mods & GLFW_MOD_ALT) {
        tb.panning = true;
    } else {
        tb.moving = true;
        Trackball::trackball(tb.lastquat, 0, 0, 0, 0);
    }

    double xpos, ypos;
    glfwGetCursorPos(window, &xpos, &ypos);
    tb.beginx = xpos;
    tb.beginy = ypos;
}

void mouse_move(GLFWwindow* window, double x, double y) {
    int W, H;
    glfwGetFramebufferSize(window, &W, &H);

    float dx = (x - tb.beginx) / (float)W;
    float dy = (tb.beginy - y) / (float)H;

    if (tb.panning) {
        tb.ortho_x += dx;
        tb.ortho_y += dy;
        tb.beginx = x;
        tb.beginy = y;
    } else if (tb.scaling) {
        tb.scalefactor *= (1.0f + dx);
        tb.beginx = x;
        tb.beginy = y;
    } else if (tb.moving) {
        Trackball::trackball(tb.lastquat,
            (2.0f * tb.beginx - W) / W, (H - 2.0f * tb.beginy) / H,
            (2.0f * x - W) / W, (H - 2.0f * y) / H);
        Trackball::add_quats(tb.lastquat, tb.curquat, tb.curquat);
        Trackball::build_rotmatrix(tb.curmat, tb.curquat);
        tb.beginx = x;
        tb.beginy = y;
    }
}

// ============================================================================
// Initialization
// ============================================================================

void initSatelliteShader() {
    // Simple shader for satellite points
    const char* sat_vshader_src = R"(
        #version 150
        in vec4 vPosition;
        uniform mat4 ModelView;
        uniform mat4 Projection;
        void main() {
            gl_Position = Projection * ModelView * vPosition;
            gl_PointSize = 8.0;
        }
    )";

    const char* sat_fshader_src = R"(
        #version 150
        uniform vec4 uColor;
        out vec4 fragColor;
        void main() {
            // Circular point
            vec2 coord = gl_PointCoord - vec2(0.5);
            if (length(coord) > 0.5) discard;
            fragColor = uColor;
        }
    )";

    GLuint vs = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vs, 1, &sat_vshader_src, NULL);
    glCompileShader(vs);

    GLuint fs = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fs, 1, &sat_fshader_src, NULL);
    glCompileShader(fs);

    sat_program = glCreateProgram();
    glAttachShader(sat_program, vs);
    glAttachShader(sat_program, fs);
    glBindFragDataLocation(sat_program, 0, "fragColor");
    glLinkProgram(sat_program);

    sat_ModelView = glGetUniformLocation(sat_program, "ModelView");
    sat_Projection = glGetUniformLocation(sat_program, "Projection");
    sat_Color = glGetUniformLocation(sat_program, "uColor");

    glGenVertexArrays(1, &sat_vao);
    glGenBuffers(1, &sat_vbo);
}

void init() {
    // Load Earth shaders
    std::string vshader = source_path + "/shaders/vshader.glsl";
    std::string fshader = source_path + "/shaders/fshader.glsl";

    GLchar* vertex_shader_source = readShaderSource(vshader.c_str());
    GLchar* fragment_shader_source = readShaderSource(fshader.c_str());

    GLuint vertex_shader = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vertex_shader, 1, (const GLchar**)&vertex_shader_source, NULL);
    glCompileShader(vertex_shader);
    check_shader_compilation(vshader, vertex_shader);

    GLuint fragment_shader = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fragment_shader, 1, (const GLchar**)&fragment_shader_source, NULL);
    glCompileShader(fragment_shader);
    check_shader_compilation(fshader, fragment_shader);

    program = glCreateProgram();
    glAttachShader(program, vertex_shader);
    glAttachShader(program, fragment_shader);
    glBindFragDataLocation(program, 0, "fragColor");
    glLinkProgram(program);
    check_program_link(program);

    glUseProgram(program);

    // Vertex attributes
    GLuint vPosition = glGetAttribLocation(program, "vPosition");
    GLuint vNormal = glGetAttribLocation(program, "vNormal");
    GLuint vTexCoord = glGetAttribLocation(program, "vTexCoord");

    // Uniforms
    glUniform4fv(glGetUniformLocation(program, "LightPosition"), 1, light_position);
    glUniform4fv(glGetUniformLocation(program, "ambient"), 1, ambient);

    ModelViewEarth = glGetUniformLocation(program, "ModelViewEarth");
    ModelViewLight = glGetUniformLocation(program, "ModelViewLight");
    NormalMatrix = glGetUniformLocation(program, "NormalMatrix");
    Projection = glGetUniformLocation(program, "Projection");

    // Create Earth mesh
    glGenVertexArrays(1, &vao);
    glGenBuffers(1, &buffer);

    mesh = new Mesh();
    mesh->makeSphere(64);  // Higher resolution for better quality

    // Load textures
    glGenTextures(1, &month_texture);
    glGenTextures(1, &night_texture);
    glGenTextures(1, &cloud_texture);
    glGenTextures(1, &perlin_texture);

    std::string earth_img = source_path + "/images/world.200405.3.png";
    loadFreeImageTexture(earth_img.c_str(), month_texture, GL_TEXTURE0);
    glUniform1i(glGetUniformLocation(program, "textureEarth"), 0);

    std::string night_img = source_path + "/images/BlackMarble.png";
    loadFreeImageTexture(night_img.c_str(), night_texture, GL_TEXTURE1);
    glUniform1i(glGetUniformLocation(program, "textureNight"), 1);

    std::string cloud_img = source_path + "/images/cloud_combined.png";
    loadFreeImageTexture(cloud_img.c_str(), cloud_texture, GL_TEXTURE2);
    glUniform1i(glGetUniformLocation(program, "textureCloud"), 2);

    std::string perlin_img = source_path + "/images/perlin_noise.png";
    loadFreeImageTexture(perlin_img.c_str(), perlin_texture, GL_TEXTURE3);
    glUniform1i(glGetUniformLocation(program, "texturePerlin"), 3);

    // Setup vertex buffer
    glBindVertexArray(vao);
    glBindBuffer(GL_ARRAY_BUFFER, buffer);

    std::size_t vertices_size = mesh->vertices.size();
    if (mesh->uvs.size() < vertices_size) {
        mesh->uvs.resize(vertices_size, vec2(0.f, 0.f));
    }
    if (mesh->normals.size() < vertices_size) {
        mesh->normals.resize(vertices_size, vec3(1.f, 1.f, 1.f));
    }

    unsigned int vertices_bytes = mesh->vertices.size() * sizeof(vec4);
    unsigned int normals_bytes = mesh->normals.size() * sizeof(vec3);
    unsigned int uv_bytes = mesh->uvs.size() * sizeof(vec2);

    glBufferData(GL_ARRAY_BUFFER, vertices_bytes + normals_bytes + uv_bytes, NULL, GL_STATIC_DRAW);
    glBufferSubData(GL_ARRAY_BUFFER, 0, vertices_bytes, &mesh->vertices[0]);
    glBufferSubData(GL_ARRAY_BUFFER, vertices_bytes, normals_bytes, &mesh->normals[0]);
    glBufferSubData(GL_ARRAY_BUFFER, vertices_bytes + normals_bytes, uv_bytes, &mesh->uvs[0]);

    glEnableVertexAttribArray(vPosition);
    glEnableVertexAttribArray(vNormal);
    glEnableVertexAttribArray(vTexCoord);

    glVertexAttribPointer(vPosition, 4, GL_FLOAT, GL_FALSE, 0, BUFFER_OFFSET(0));
    glVertexAttribPointer(vNormal, 3, GL_FLOAT, GL_FALSE, 0, BUFFER_OFFSET(vertices_bytes));
    glVertexAttribPointer(vTexCoord, 2, GL_FLOAT, GL_FALSE, 0, BUFFER_OFFSET(vertices_bytes + normals_bytes));

    // OpenGL state
    glEnable(GL_DEPTH_TEST);
    glEnable(GL_PROGRAM_POINT_SIZE);
    glShadeModel(GL_SMOOTH);
    glClearColor(0.0, 0.0, 0.02, 1.0);  // Very dark blue background

    // Initialize state
    animate_time = 0.0;
    rotation_angle = 0.0;
    wireframe = false;

    // Initialize satellite shader
    initSatelliteShader();

    // Try to load trajectory data
    std::string traj_file = source_path + "/data/trajectories.csv";
    loadTrajectoryData(traj_file);
}

// ============================================================================
// Animation
// ============================================================================

void animate() {
    if (paused) return;

    if (glfwGetTime() > (1.0 / 60.0)) {
        animate_time += 0.0001f * playback_speed;

        const float sun_cycle_seconds = 25.0f;
        rotation_angle += (360.0f / sun_cycle_seconds) * (1.0f / 60.0f) * playback_speed;

        // Earth auto-rotation
        if (auto_rotate) {
            earth_rotation += earth_rotation_speed * playback_speed;
            if (earth_rotation >= 360.0f) earth_rotation -= 360.0f;
        }

        // Advance satellite frame
        if (!satellites.empty() && satellites[0].positions.size() > 0) {
            global_frame++;
            if (global_frame >= (int)satellites[0].positions.size()) {
                global_frame = 0;  // Loop
            }
        }

        glfwSetTime(0.0);
    }
}

void updateWindowTitle(GLFWwindow* window) {
    char title[256];
    snprintf(title, sizeof(title), 
        "Earth Viewer | Sats: %s | Trails: %s | Rotate: %s | Speed: %.1fx | [H] Help",
        show_satellites ? "ON" : "OFF",
        show_trails ? "ON" : "OFF", 
        auto_rotate ? "ON" : "OFF",
        playback_speed);
    glfwSetWindowTitle(window, title);
}

// ============================================================================
// Rendering
// ============================================================================

void drawSatellites(const mat4& user_MV, const mat4& projection) {
    if (!show_satellites || satellites.empty()) return;

    glUseProgram(sat_program);
    glUniformMatrix4fv(sat_Projection, 1, GL_TRUE, projection);

    glBindVertexArray(sat_vao);
    glBindBuffer(GL_ARRAY_BUFFER, sat_vbo);

    GLuint vPos = glGetAttribLocation(sat_program, "vPosition");
    glEnableVertexAttribArray(vPos);

    for (const auto& sat : satellites) {
        if (sat.positions.empty()) continue;

        // Draw trail
        if (show_trails) {
            int start = std::max(0, global_frame - trail_length);
            int count = global_frame - start;

            if (count > 0) {
                std::vector<vec4> trail_points;
                for (int i = start; i < global_frame; i++) {
                    const auto& p = sat.positions[i];
                    trail_points.push_back(vec4(p.x, p.y, p.z, 1.0f));
                }

                glBufferData(GL_ARRAY_BUFFER, trail_points.size() * sizeof(vec4),
                    &trail_points[0], GL_DYNAMIC_DRAW);
                glVertexAttribPointer(vPos, 4, GL_FLOAT, GL_FALSE, 0, 0);

                glUniformMatrix4fv(sat_ModelView, 1, GL_TRUE, user_MV);
                glUniform4f(sat_Color, sat.color.x * 0.5f, sat.color.y * 0.5f, sat.color.z * 0.5f, 0.5f);

                glDrawArrays(GL_LINE_STRIP, 0, trail_points.size());
            }
        }

        // Draw current position
        const auto& pos = sat.positions[global_frame];
        vec4 point(pos.x, pos.y, pos.z, 1.0f);

        glBufferData(GL_ARRAY_BUFFER, sizeof(vec4), &point, GL_DYNAMIC_DRAW);
        glVertexAttribPointer(vPos, 4, GL_FLOAT, GL_FALSE, 0, 0);

        glUniformMatrix4fv(sat_ModelView, 1, GL_TRUE, user_MV);
        glUniform4f(sat_Color, sat.color.x, sat.color.y, sat.color.z, 1.0f);

        glDrawArrays(GL_POINTS, 0, 1);
    }

    glDisableVertexAttribArray(vPos);
}

// ============================================================================
// Main
// ============================================================================

int main(int argc, char* argv[]) {
    GLFWwindow* window;

    glfwSetErrorCallback(error_callback);

    if (!glfwInit()) exit(EXIT_FAILURE);

    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 2);
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    glfwWindowHint(GLFW_SAMPLES, 4);

    window = glfwCreateWindow(1280, 960, "Orbital Visualization Platform - Earth Viewer", NULL, NULL);
    if (!window) {
        glfwTerminate();
        exit(EXIT_FAILURE);
    }

    glfwSetKeyCallback(window, key_callback);
    glfwSetMouseButtonCallback(window, mouse_click);
    glfwSetCursorPosCallback(window, mouse_move);

    glfwMakeContextCurrent(window);
    gladLoadGLLoader((GLADloadproc)glfwGetProcAddress);
    glfwSwapInterval(1);

    std::cout << "=== Orbital Visualization Platform ===" << std::endl;
    std::cout << "Controls:" << std::endl;
    std::cout << "  Mouse drag    - Rotate view" << std::endl;
    std::cout << "  Shift + drag  - Zoom" << std::endl;
    std::cout << "  Alt + drag    - Pan" << std::endl;
    std::cout << "  SPACE         - Pause/Play" << std::endl;
    std::cout << "  A             - Toggle auto-rotate" << std::endl;
    std::cout << "  S             - Toggle satellites" << std::endl;
    std::cout << "  T             - Toggle trails" << std::endl;
    std::cout << "  W             - Toggle wireframe" << std::endl;
    std::cout << "  UP/DOWN       - Satellite animation speed" << std::endl;
    std::cout << "  LEFT/RIGHT    - Earth rotation speed" << std::endl;
    std::cout << "  R             - Reset animation" << std::endl;
    std::cout << "  H             - Show help" << std::endl;
    std::cout << "  ESC           - Quit" << std::endl;
    std::cout << "=======================================" << std::endl;
    std::cout << "Satellites loaded: " << satellites.size() << std::endl;

    init();

    while (!glfwWindowShouldClose(window)) {
        if (wireframe) {
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
        } else {
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);
        }

        int width, height;
        glfwGetFramebufferSize(window, &width, &height);
        glViewport(0, 0, width, height);

        GLfloat aspect = GLfloat(width) / height;
        mat4 projection = Perspective(45.0, aspect, 0.1, 100.0);

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        const vec3 viewer_pos(0.0, 0.0, 3.0);

        mat4 track_ball = mat4(
            tb.curmat[0][0], tb.curmat[1][0], tb.curmat[2][0], tb.curmat[3][0],
            tb.curmat[0][1], tb.curmat[1][1], tb.curmat[2][1], tb.curmat[3][1],
            tb.curmat[0][2], tb.curmat[1][2], tb.curmat[2][2], tb.curmat[3][2],
            tb.curmat[0][3], tb.curmat[1][3], tb.curmat[2][3], tb.curmat[3][3]);

        mat4 user_MV = Translate(-viewer_pos) *
            Translate(tb.ortho_x, tb.ortho_y, 0.0) *
            track_ball *
            Scale(tb.scalefactor, tb.scalefactor, tb.scalefactor);

        animate();
        
        // Update window title with current state
        static int title_update_counter = 0;
        if (++title_update_counter >= 30) {  // Update every 30 frames
            updateWindowTitle(window);
            title_update_counter = 0;
        }

        // Earth rotation matrix (around Y axis)
        float earth_rad = earth_rotation * (float)(M_PI / 180.0);
        mat4 earth_rot = mat4(
            cos(earth_rad), 0, sin(earth_rad), 0,
            0, 1, 0, 0,
            -sin(earth_rad), 0, cos(earth_rad), 0,
            0, 0, 0, 1
        );

        // Update sun position
        glUseProgram(program);
        glUniform1f(glGetUniformLocation(program, "animate_time"), animate_time);
        float radians = rotation_angle * (float)(M_PI / 180.0);
        vec4 moving_light = vec4(10.0f * cos(radians), 0.0f, 10.0f * sin(radians), 1.0f);
        glUniform4fv(glGetUniformLocation(program, "LightPosition"), 1, moving_light);

        // Draw Earth with rotation
        mat4 earth_MV = user_MV * earth_rot * mesh->model_view;
        glBindVertexArray(vao);
        glUniformMatrix4fv(ModelViewEarth, 1, GL_TRUE, earth_MV);
        glUniformMatrix4fv(ModelViewLight, 1, GL_TRUE, earth_MV);
        glUniformMatrix4fv(Projection, 1, GL_TRUE, projection);
        glUniformMatrix4fv(NormalMatrix, 1, GL_TRUE, transpose(invert(earth_MV)));
        glDrawArrays(GL_TRIANGLES, 0, mesh->vertices.size());

        // Draw satellites (they orbit independently of Earth rotation)
        drawSatellites(user_MV, projection);

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    delete mesh;
    glfwDestroyWindow(window);
    glfwTerminate();
    exit(EXIT_SUCCESS);
}
