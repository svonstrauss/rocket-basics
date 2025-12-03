#version 150

uniform vec4 ambient;
uniform vec4 LightPosition;

in vec4 pos;
in vec4 N;
in vec2 texCoord;

uniform mat4 ModelViewLight;

uniform sampler2D textureEarth;
uniform sampler2D textureNight;
uniform sampler2D textureCloud;
uniform sampler2D texturePerlin;

uniform float animate_time;


out vec4 fragColor;

void main()
{
  // Lambertian diffuse term
  vec3 L = normalize( (ModelViewLight * LightPosition).xyz - pos.xyz );
  vec3 Nn = normalize(N.xyz);
  float lambert = max(dot(Nn, L), 0.0);

  // Base day and night textures
  vec3 dayTex   = texture(textureEarth, texCoord).rgb;
  vec3 nightTex = texture(textureNight, texCoord).rgb;

  // Compute smooth night intensity (no lights at midday)
  float nightIntensity = pow(1.0 - lambert, 3.0);
  vec3 base = dayTex * lambert + nightTex * nightIntensity;

  // Clouds: add white cloud map (optionally drifted with noise)
  vec2 noiseUV = texCoord * 2.0;
  vec2 noise = texture(texturePerlin, noiseUV).rg - vec2(0.5);
  vec2 cloudUV = texCoord + vec2(animate_time * 0.02, 0.0) + noise * 0.02;
  vec3 clouds = texture(textureCloud, cloudUV).rgb; // white = clouds

  vec3 color = clamp(base + clouds, 0.0, 1.0);
  color = clamp(color + ambient.rgb, 0.0, 1.0);

  fragColor = vec4(color, 1.0);
}

