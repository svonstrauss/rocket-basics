Perfect. I’ll now build a detailed day-by-day plan for Modules 2 through 6 and the Capstone, maintaining the same structure as Module 1.

Each module will include:

Ultimate SpaceX-Focused Self-Study Program in
 Space Systems & Aerospace Engineering
 1
 Overview: This comprehensive 6-module, ~1-year self-study roadmap is laser-focused on building the skills
 and portfolio needed to land a role at SpaceX. It emphasizes showcase projects (10–12 in total + a capstone)
 over theory alone – aligning with SpaceX’s hiring philosophy that “clear evidence of exceptional ability”
 (e.g. impressive projects) matters more than degrees . Each module culminates in one or two GitHub
ready projects (with code, README, plots, and demo videos) demonstrating skills in math, physics, coding,
 and aerospace. We’ve also integrated only essential extras: real-world tools (e.g. NASA’s GMAT, STK), relevant
 certifications, and networking habits – all based on SpaceX career page insights (emphasis on Python/ML
 for autonomy, systems engineering for reusability, etc.). No fluff: every task ties into skills SpaceX looks for
 (e.g. building simulators, analyzing orbits) or bolsters your ability to showcase those skills. By the end, you’ll
 have a portfolio that proves you can “develop highly reliable autonomous software systems and the
 simulations required to validate them” – exactly the kind of work SpaceX engineers do . Let’s get
 started! 
Preparation and Daily Routine Tips (Day 0)
 2
 Before diving into Module 1, spend a “Day 0” on setup and planning to maximize your efficiency and keep
 the SpaceX mission in sight throughout:
 • 
• 
• 
• 
• 
• 
Initial Setup (Day 0, ~2 hours): Install essential tools like Python (Anaconda distribution for
 scientific computing) and set up a development environment (IDE or Jupyter Notebooks). Download
 the Briggs calculus e-book (for math refreshers) and bookmark key resources (MIT OCW, NASA
 sources, etc.). Create a GitHub repository called “rocket-basics” with a README template describing
 your first project (e.g. “Rocket Ascent Simulator – Simulating a Starship-like launch trajectory with
 differential equations; ties to SpaceX’s flip maneuvers”). Also ensure you have libraries like NumPy,
 Matplotlib, and a simple ML library (scikit-learn or XGBoost) installed – you’ll use these for numerical
 simulation and basic machine learning tasks.
 Daily Study Routine: Aim for 8–10 hours per week, spread across 7 days (about 1.5 hours per day,
 but adjust as needed). Each study day will typically include:
 Warm-Up (10 min): Start with a quick refresher – e.g. a short Khan Academy or 3Blue1Brown video on
 the day’s math/physics concept – to get in the right mindset.
 Learning (1–2 hours): Do the assigned readings and watch recommended videos/lectures for that
 day’s topic.
 Practice (1–2 hours): Solve a few practice problems or exercises to solidify the concepts. Focus on
 problems with real-world context (many from Briggs or MIT OCW problem sets are suggested).
 Coding (1 hour): Implement a bite-sized coding project or simulation related to the topic (e.g. writing
 a script to plot a trajectory, solve an equation, or visualize data). Gradually, these will build
 components of your showcase projects.
 1
• 
• 
• 
• 
Review & SpaceX Tie-In (30 min): End the day by quizzing yourself (ensure you can solve at least a
 couple problems without notes) and reflect on how the day’s content ties into SpaceX
 applications. Write a few sentences in your Notion journal connecting theory to practice (e.g.
 “Today’s lesson on orbital ellipses helps in understanding Starship’s parking orbit for refueling.”).
 Pacing and Skipping: The program is rigorous but flexible. If you’re already confident in a topic, feel
 free to skip ahead or condense. For example, if you’re strong in single-variable calculus, you might
 compress or skip the first week of Module 1 (basic calculus review). Each module has checkpoint
 quizzes (e.g. end-of-week quizzes aiming for ~85% correct); use these to decide if you can move
 faster. Conversely, if you need more time on a hard concept, take it – mastery is key.
 Motivation Hacks: Keep the SpaceX inspiration burning daily. Watch a 5-minute clip of a SpaceX
 launch or Starship test each day and note one connection to what you’re learning. This could be as
 direct as “vector calculus is behind Starship’s 3D trajectory calculations” or as broad as “solving tough
 problems like these is how SpaceX succeeds.” This habit not only reinforces your learning with real
world examples but also reminds you why you’re putting in the work. Pro tip: Use a whiteboard or
 notebook to jot quick ideas during these videos – you might even come up with project ideas or
 questions to explore later.
 Accountability: Track everything in a Notion or Trello board. Create a checklist for each day’s tasks
 and tick them off to visualize progress. Consider writing a brief daily journal entry (what you did, any
 issues, what excited you) – by Module 6, you’ll love scrolling back to see how far you’ve come. If a day
 or week feels too easy, challenge yourself with an extra problem or a deeper dive into one of the
 “optional” resources listed. If it feels overwhelming, remember it’s okay to stretch a topic over two
 days or take a rest day – consistency matters more than perfection.
 Now, with your environment ready and a solid routine in place, let’s launch into Module 1.
 Module 1: Foundations in Math, Physics, and Computation (8
 Weeks) – Building Rocket Basics
 Module Overview: Module 1 establishes the core math and physics needed for rocketry, while sharpening
 your programming skills. By the end of 8 weeks, you’ll have built two portfolio-worthy projects from scratch– a 3D Rocket Ascent Simulator and a Conic Orbit Visualizer – showcasing your grasp of calculus, vectors,
 and basic differential equations as they apply to real SpaceX-inspired problems. The focus is on essentials:
 no abstract fluff, only concepts directly feeding into aerospace applications (e.g. parametric equations for
 trajectories, forces in 3D, basic orbital conics, introductory ODEs for motion). SpaceX tie-ins are highlighted
 throughout to keep your work relevant. (If you’re already comfortable with the basics, you can accelerate this
 module by combining days or skipping review-heavy sections. But don’t skip the projects!)
 Week 1: Parametric Equations & Conic Sections – Orbit Shapes for Starship
 Week Goal: Gain comfort with parametric and polar representations of curves, especially conic sections
 (circles, ellipses, parabolas, hyperbolas). These are the mathematical foundations for orbits and trajectories.
 2
By week’s end, you’ll write a simple Python script to visualize these conic orbits, building intuition for how a
 Starship’s trajectory might look for different energies (from circular low orbit to hyperbolic escape).
 • 
• 
• 
• 
• 
• 
• 
• 
• 
• 
Day 1 – Focus: Intro to Parametric Equations
 Readings/Videos (1.5 hrs): Read Briggs Calculus Ch. 11.1 on parametric equations (about 10 pages
 covering how to represent curves like projectile paths parametrically). Also watch an introductory
 segment of MIT’s 18.01 Single Variable Calculus on parametric curves or an OCW video on
 coordinate systems (~30 min) to reinforce the concept. 
Exercises (1 hr): Solve ~4 problems from Briggs 11.1. For example, one problem might give a
 parametric form of a rocket’s flight path and ask you to eliminate the parameter or find the
 maximum height. Work through these to practice switching between parametric and Cartesian
 forms. 
Coding (1 hr): Begin your “conic-visualizer.py” script. Today, implement a basic parametric plotter.
 Start simple: code a parametric equation for a circle (e.g. $x = r\cos t$, $y = r\sin t$) to simulate an
 ideal circular orbit. Use Matplotlib to plot it. This will set up the structure (you can extend the code
 for ellipses, etc., in later days). 
Review/SpaceX Tie-In (30 min): Do a quick self-quiz: write down 2 short questions for yourself (e.g.
 “How do parametric equations simplify analyzing motion compared to $y=f(x)$?” and “Give one example
 of a real rocket trajectory that is easier to express parametrically.”). Ensure you can answer them. Tie-in:
 Jot down how SpaceX might use parametric equations – e.g. plotting a Starship’s curved ascent
 where $x(t), y(t), z(t)$ define its position over time. Reflection: Parametric equations let us easily model
 a rocket’s path over time, which is exactly how guidance software tracks rockets. This connection will keep
 the math aligned with your end goal.
 Day 2 – Focus: Polar Coordinates & Orbits
 Readings/Videos (1.5 hrs): Read Briggs Ch. 11.2 on polar coordinates (8 pages focusing on how curves
 are described with $r(\theta)$ – crucial for orbits where we often use $r$ vs. angle). Complement this
 with a short lecture excerpt (20 min) from Walter Lewin’s MIT physics series – specifically, part of
 Lecture 22 where he introduces polar equations for orbits (Lewin has a famous segment on
 planetary orbits and ellipses in polar form). 
Exercises (1 hr): Solve ~4 problems from Briggs 11.2. These might include converting between polar
 and Cartesian or finding slopes of polar graphs. Pick ones that resemble orbital trajectory problems
 (e.g. an example of a spacecraft trajectory given by $r(\theta) = \frac{a(1-e^2)}{1+e\cos\theta}$,
 which is the polar form of an ellipse). Solve for specific points like periapsis distance, etc. 
Coding (1 hr): Extend “conic-visualizer.py” to handle polar input. For instance, allow the user to input
 an eccentricity $e$ and semi-major axis $a$, then plot the resulting curve defined by the polar
 equation of a conic: $r(\theta) = \frac{a(1-e^2)}{1 + e\cos\theta}$. Test it by plotting an ellipse (0 < e <
 1), a parabola (e = 1, perhaps truncated range), and a hyperbola (e > 1) – to visualize how orbit
 shapes change with eccentricity. 
Review/SpaceX Tie-In (30 min): Quiz yourself on 2 quick items (e.g. “How do you identify a conic section
 (circle/ellipse/parabola/hyperbola) from its polar equation?”). Tie-in: Think about why polar coordinates
 are natural for orbits – SpaceX mission planners use polar equations to optimize launch trajectories
 (angles, etc.). Note in your journal: “Polar coordinates let us handle rocket trajectories that go out and
 back (radial distance as a function of angle is great for analyzing orbital insertion angles).” This is directly
 3
relevant when considering, say, the orbital insertion of Starship – the angle at which it needs to be
 when cutting engines to achieve a stable orbit can be calculated in polar form.
 • 
• 
• 
• 
• 
• 
• 
• 
• 
Day 3 – Focus: Calculus in Polar Coordinates (Rates of Change)
 Readings/Videos (1 hr): Read Briggs Ch. 11.3, which covers derivatives and slopes for polar curves (7
 pages). This is important for finding velocity components or slopes (dy/dx) in polar form – think of a
 rocket’s radial vs tangential velocity. No heavy videos today; the reading itself is concise. 
Exercises (1.5 hrs): Solve ~5 problems from Briggs 11.3. These likely involve computing $\frac{dy}{dx}$
 or speed for a particle moving along a polar curve. For example, given $r(\theta)$ of a trajectory, find
 where the slope is zero (horizontal flight) or undefined (vertical climb) – scenarios a rocket
 experiences. One problem might explicitly ask for the speed along a polar curve at a certain angle;
 solve it to practice using the formula for velocity in polar coords ($v^2 = \dot r^2 + (r\dot\theta)^2$ if
 you want to connect to physics). 
Coding (1 hr): Add a feature to “conic-visualizer.py”: compute and display the orbital speed at
 various points. For a given polar orbit $r(\theta)$, derive $dr/d\theta$ and use it to estimate how fast
 an object moves along the curve if $\theta$ changes at a constant rate. (This is a bit of a
 simplification of true orbital mechanics, but it’s great practice in relating calculus to motion.) For
 example, differentiate the ellipse equation to find how $r$ changes with $\theta$, and maybe
 compute velocity at periapsis vs apoapsis qualitatively. 
Review/SpaceX Tie-In (30 min): Quiz 3 small items (e.g. “Write the formula for dy/dx in polar coordinates.”,
 “Why do orbits have fastest speed at periapsis?”). Check your answers. SpaceX tie-in: Reflect on how
 understanding rates (derivatives) in polar form helps in rocketry – e.g. “When Starship is in an elliptical
 transfer orbit, its velocity changes: calculus helps predict when to burn engines to adjust that orbit.”
 Connecting the math of rates to burn timing and throttle control in Starship’s ascent/descent
 makes the calculus more tangible.
 Day 4 – Focus: Conic Sections as Orbits
 Readings/Videos (1 hr): Read Briggs Ch. 11.4, about 10 pages on the classical conic sections (circle,
 ellipse, parabola, hyperbola) and their properties. As you read, mentally link each conic to a type of
 orbit: circle = low Earth orbit, ellipse = transfer orbit or bound orbit, hyperbola = escape trajectory,
 parabola = borderline escape. If available, glance at an online resource or short video on orbital
 trajectories (for instance, NASA’s or ESA’s introductory materials on orbits) – but the Briggs text +
 your prior work is likely enough. 
Exercises (1.5 hrs): Solve ~5 problems from Briggs 11.4. These could include finding the eccentricity
 given an equation, or vice versa, or computing intersections of an orbit trajectory with axes. A
 particularly relevant exercise: given an $e > 1$ (hyperbolic trajectory) equation, find asymptotes or
 other parameters – analogously, this relates to escape trajectories for interplanetary missions (like
 Starship’s future Mars departure burns). Another example: calculate the eccentricity needed for an
 ellipse that goes from Earth’s orbit to Mars’ orbit (tying in some basic astrodynamics). 
Coding (1 hr): Finish the core features of “conic-visualizer.py.” By now, your script plots conics and
 maybe computes speeds. Add some polish: perhaps the ability to input different orbital parameters
 (like semi-major axis length, eccentricity) and annotate key points (perihelion/perigee, aphelion). For
 fun, plug in values that approximate a known orbit: e.g. Earth’s orbit around the Sun (e ~ 0.0167 
nearly circular), or a highly eccentric orbit. See what the plot looks like, and ensure your code can
 4
handle e=0 (circle) up to e→1 (parabolic) or e>1. Save a few example plots (you can later include
 these in your GitHub repo or even in your eventual SpaceX application portfolio). 
• 
• 
• 
• 
• 
• 
• 
Review/SpaceX Tie-In (30 min): Quiz 3 problems to review the week’s breadth – e.g. “If Starship is on a
 transfer ellipse to Mars, what type of conic and what is roughly its eccentricity?”, “How does increasing
 eccentricity affect the shape of an orbit, and what does that mean for mission profiles?” Write brief
 answers. Tie-in: Note how conic sections appear in Starship’s missions: a Starship on a Mars
 transfer will start in an elliptical orbit around Earth, then a hyperbolic escape. When you simulate
 these conics, you’re essentially simulating parts of a Starship’s journey. In your reflection journal,
 connect this to the real physics: “Conics (ellipse/hyperbola) are the mathematical backbone of mission
 trajectories – by plotting these, I’m laying groundwork for simulating a Starship going to Mars.”
 Day 5 – Build & Test the Orbit Visualizer
 Readings/Videos (0.5 hr): Skim back through Briggs Ch. 11 (sections 1–4) to consolidate what you
 learned. Re-watch any tricky portion of a video from earlier in the week if needed. The goal is to
 ensure you haven’t missed a key point before applying everything in code. 
Exercises (1 hr): Solve 3 mixed problems covering the whole week (parametric, polar, conics). For
 example, one problem of each type: convert a parametric set to Cartesian, find a slope in polar, and
 identify a conic from an equation. Doing a mixed set cements your ability to jump between concepts– just like you might need to when solving an integrated rocket problem (where geometry and
 calculus come together). 
Coding (2 hrs): Today, treat as a mini “hackathon” to polish your “conic-visualizer.py” into a shareable
 project:
 ◦ 
◦ 
◦ 
◦ 
Ensure the code is clean and commented. Add an input interface (could be as simple as
 prompting in the console, or a Jupyter notebook UI) to choose conic type and parameters.
 Include sample outputs: e.g. when the script runs, it might produce a plot of a circular orbit
 vs an elliptical transfer orbit for comparison.
 Test edge cases (what if user inputs weird values? Make it robust enough for your use).
 If you’re comfortable, add one advanced feature: maybe the ability to animate the orbit (plot
 a point moving along the curve) to mimic a spacecraft traveling along it. This could be done
 with a simple loop updating the plot – a nice touch for a demo.
 Review/SpaceX Tie-In (30 min): Run your finalized script and observe the results. Write a short
 summary for your README: what does this visualizer do, and how does it tie to SpaceX? For example:
 “This tool visualizes orbital paths (circles, ellipses, hyperbolas). SpaceX relevance: helps illustrate
 trajectories like Starship’s parking orbit vs. an escape path for a Mars mission.” Also, note any machine
 learning idea that arose (the plan suggested “note ML potential” – e.g., could you use ML to optimize an
 orbit? Perhaps predict the required eccentricity for a given mission constraint. Just jot this down as a
 future idea, since you have ML background). Commit your code to GitHub with a clear commit
 message.
 Day 6 – Integrate a Touch of ML (Optional/Advanced)
 Note: This day is a bit more advanced and integrates your machine learning background. It’s marked
 optional – if you’re feeling the week was heavy, you can skip or shorten this. But it’s included to
 leverage your existing skills and make your project stand out.
 5
• 
Readings/Videos (1 hr): Skim an online resource on basic orbital mechanics or celestial mechanics that
 ties orbits to energy (for intuition – about 20 pages or a couple of articles). Also, if available, read a
 tutorial or watch a short video on using scikit-learn’s Random Forest (since you plan to use
 Random Forest for some optimizations) – just to refresh how to implement and interpret one for
 regression tasks.
 • 
• 
• 
• 
• 
• 
• 
• 
Exercises (1 hr): Do 3 small problems that connect orbits to optimization. For example: “If you vary
 eccentricity, how does time of flight change?” or “Given two orbits, which requires more delta-V?” – these
 are conceptual, but thinking through them sets up the ML application.
 Coding (1.5 hrs): Augment your “conic-visualizer” project with a simple ML experiment: use a
 Random Forest model to predict something like optimal orbital parameters. For instance, you
 could generate a synthetic dataset where inputs are orbital parameters (a, e) and output is some
 performance metric (say, delta-V required, or time of flight for a transfer). Train a
 RandomForestRegressor on this (even if the data is self-generated from physics formulas). Then use
 it to predict an optimal orbit for a scenario (like minimum delta-V). This is a bit exploratory; the key is
 to show you can combine physics with ML. Even a very basic attempt (with dummy data) is fine – it’s
 more about showcasing that you know how to integrate ML into engineering problems.
 Review/SpaceX Tie-In (30 min): Reflect on how ML is used by SpaceX (they likely use ML for things like
 trajectory optimization, anomaly detection, etc.). Write a note on how your Random Forest
 experiment could be a proto-example of “using ML to optimize fuel efficiency for trajectories”,
 analogous to how SpaceX might let algorithms fine-tune an approach for maximum reuse or fuel
 savings. This will be great to mention if interviewing – that you attempted an ML integration in an
 orbital context.
 Day 7 – Week 1 Review and Portfolio Update
 Review (0.5 hr): Go over all your notes from Week 1. Summarize in a half-page the key mathematical
 concepts (parametric equations, polar coordinates, conic sections) and why they matter for space
 systems. This solidifies your own understanding and gives you a “cheat sheet” to look back on.
 Week 1 Quiz (1 hr): Take a self-made quiz of ~10 problems covering everything from the week. Use a
 mix: some calculus (derivatives, etc.), some conceptual (identify orbit types), some short answer.
 Grade yourself brutally – aim for 85% or higher to ensure you’re ready to move on. If below that,
 identify weak spots and consider redoing a couple of exercises or reviewing that topic next week.
 Project Demo (1 hr): Record a short 2-minute demo video of your Conic Orbit Visualizer (Project 2
 for this module). This can be as simple as a screen recording where you run the script for a couple of
 cases (circle vs. ellipse vs. hyperbola) and narrate what’s happening. Emphasize the SpaceX tie-in in
 your narration: e.g., “Here I input an eccentricity of 1.2 to simulate a hyperbolic escape trajectory – this
 would be like a Starship doing a trans-Martian injection.” Even though this video is just for practice now,
 it’s good to get in the habit; you might use it (or re-record a polished version) when you start
 reaching out to recruiters or networking.
 Portfolio Update & Tie-In: Upload your code to GitHub if you haven’t already, and update the README
 with images (you can add a plot image) and instructions. Title it clearly and mention SpaceX: e.g., 
“Orbital Conic Sections Visualizer – simulating orbits (Starship trajectory examples)”. This way,
 anyone glancing at your GitHub sees the relevance. In your Notion journal, write a short reflection
 on Week 1: “Highlights: Created a tool to visualize orbits. Challenges: polar calculus was tricky but
 manageable. SpaceX Tie: now I understand how elliptical vs hyperbolic trajectories differ – critical for
 missions beyond Earth.” If you aced your quiz, treat yourself – Week 1 is done! If not, plan a quick
 refresher for the weekend before diving into Week 2.
 6
Week 2: Vectors and 3D Motion – Rocket Trajectories in Three Dimensions
 Week Goal: Apply vector math to model real 3D motion of rockets. This week bridges calculus and physics:
 you’ll use vectors, dot/cross products, and basic kinematics in 3D to simulate projectile motion with gravity
 and drag. By the end of Week 2, you’ll have a functioning “Projectile/Rocket Ascent Simulator” script
 (Project 1 for this module) that can simulate a rocket’s flight path given thrust, gravity, and drag – basically a
 simplified Starship launch. You’ll also practice integrating basic machine learning by predicting optimal
 launch angles or parameters using the simulator data.
 • 
• 
• 
• 
• 
• 
• 
• 
• 
Day 8 – Focus: 3D Vector Basics
 Readings/Videos (1.5 hrs): Read Briggs Ch. 12.2 on 3D vectors and coordinate geometry (about 10
 pages covering vector definitions, addition, unit vectors, etc. in 3-space). Watch a visual explanation
 from 3Blue1Brown (Videos 1–2 of the Essence of Linear Algebra series, ~30 min) to get an intuitive
 feel for vectors in space and their operations. 
Exercises (1 hr): Solve ~4 problems from Briggs 12.2 focusing on vector operations. For instance,
 compute resultant forces given several component vectors – think of a problem like “a rocket is
 subject to gravitational force (vector down) and thrust (vector up and angled); find the net vector”.
 This will reinforce head-to-tail addition and unit vector components (i, j, k). 
Coding (1 hr): Start a new Python script “projectile_sim.py”. Today, implement basic vector
 operations using NumPy: perhaps write functions for vector addition, dot product, and cross product
 (even though NumPy has them, doing it yourself solidifies understanding). Then, simulate a very
 basic 2D projectile motion: define a position vector r and velocity vector v for a rocket, and update
 them over small time steps under gravity (no drag or thrust yet, just a simple cannonball trajectory).
 Plot the trajectory in 2D to ensure it looks parabolic. This sets the foundation for adding complexity. 
Review/SpaceX Tie-In (30 min): Quiz yourself with 2 quick vector questions (e.g. “What’s the difference
 between a vector’s magnitude and its components?”, “How do you compute a unit vector in the direction of
 (a,b,c)?”). Tie-in: Note how vectors are used for Starship’s flight: the rocket’s velocity, acceleration,
 thrust direction – all are vectors. In your reflection, write: “Understanding 3D vectors means I can
 calculate Starship’s trajectory in three axes. For example, today’s sim (though 2D) is the start of a 3D flight
 simulator for a rocket.” Knowing that SpaceX deals with vector quantities (force, momentum, etc.)
 daily gives purpose to these basics.
 Day 9 – Focus: Dot & Cross Products (Forces and Torque)
 Readings/Videos (1 hr): Read Briggs Ch. 12.3 and 12.4 (about 12 pages combined) covering the dot
 product (and projections) and cross product (with applications like torque). These operations are
 vital: dot products for finding components of forces, cross for moments/torque and determining
 perpendicular directions. Watch 3Blue1Brown’s next couple of videos (3–4, ~20 min) which brilliantly
 visualize dot and cross products. 
Exercises (1.5 hrs): Solve ~5 problems from these sections. For dot product: maybe find the work done
 by a force vector acting along a displacement (simulating computing work done by thrust over some
 distance). For cross product: solve a problem about torque or angular momentum – e.g., given a
 thrust vector and lever arm, find the resulting torque (this mirrors a Starship gimbaling its engines 
the cross product gives the rotational effect). Also practice determining if vectors are orthogonal
 (dot=0) or parallel (cross=0) – useful in checking alignment of forces. 
Coding (1 hr): Expand “projectile_sim.py.” Add calculations for dot and cross product in code (if you
 haven’t already). Then, incorporate a simple torque simulation: For instance, given a rocket thrust
 7
vector that’s slightly off-center, compute the torque about the rocket’s center of mass (cross product
 of lever arm and thrust). While a full 6-DOF simulation is too much, just printing out the torque
 vector for some test values is insightful. Additionally, use dot products to project velocity onto
 different axes (for example, check the vertical component of velocity at launch vs later). These
 additions aren’t full features, but they enrich your understanding and could be stepping stones if
 you later expand the simulator (e.g., to include rocket pitching). 
• 
• 
• 
• 
• 
• 
Review/SpaceX Tie-In (30 min): Quiz 3 items: perhaps a quick dot product calc, a cross product
 direction determination, and a conceptual question (“why is cross product useful in rocket engine
 alignment?”). Tie-in: Write down how engine gimbal and torque relate: “Cross products model
 Starship’s engine gimbal creating a torque to adjust its orientation.” SpaceX famously uses gimballing
 for control – you now see the math behind it. In your notes, connect this to what you might simulate
 later (maybe in Module 4 when dealing with landing dynamics or in a subsystem trade study about
 control authority).
 Day 10 – Focus: Vector-Valued Functions & Space Curves
 Readings/Videos (1 hr): Read Briggs Ch. 12.5 and 12.6 (about 10 pages total) which introduce vector
valued functions (parametric curves in 3D) and the calculus of these curves (velocity, acceleration as
 derivatives of position vector). This ties directly into projectile motion where r(t) is the position of
 your rocket over time. No specific video required today, but if you find calculus of parametric curves
 confusing, consult MIT OCW or Khan Academy on vector functions (optional ~20 min). 
Exercises (1 hr): Solve ~4 problems involving vector functions. E.g., given r(t) for a particle (maybe a
 helix or something), find velocity v(t) and acceleration a(t). Or determine speed at a certain time
 (magnitude of v). Ideally, use a projectile example: “A rocket’s position is given by r(t) = (v0cosθ * t,
 v0sinθ * t - ½gt^2) — find when it hits ground and how far downrange.” That is essentially deriving
 range, etc., from parametric equations – a classic result you should know. 
Coding (1.5 hrs): Upgrade “projectile_sim.py” to truly simulate a 3D trajectory as a vector function
 of time. Implement the following:
 ◦ 
◦ 
◦ 
◦ 
◦ 
Treat position r and velocity v as 3D vectors [x,y,z]. For simplicity, you can keep motion in a
 vertical plane for now (so y (horizontal), z (vertical), with x=0 or constant), or go full 3D by
 allowing an initial launch angle in two directions (elevation and azimuth).
 Use a simple time-step loop (Euler integration) to update r and v: 
v = v + a*dt , 
r = r + v*dt . Include gravity g = 9.81 m/s² downward in the acceleration a. Ignore air
 drag for now (that’s for tomorrow).
 Allow the user to input initial speed and angle(s), or just hardcode a test scenario (e.g., launch
 speed = 500 m/s at 45°) to generate a trajectory.
 After simulating, have the code output key results: max height, range, flight time. This coding
 task essentially creates the backbone of a rocket ascent simulator (albeit without thrust
 beyond initial impulse yet).
 Plot the trajectory in a 2D graph (distance vs height). If you do a full 3D sim, you could plot
 ground track (x vs y) or altitude over ground distance.
 Review/SpaceX Tie-In (30 min): Test your simulation with a couple of different angles. Quiz yourself:
 “What equation does my sim’s results approach for 45° in vacuum (should match projectile range
 formula)?” Ensure it makes sense. Tie-in: Journal about how vector functions let you simulate a
 Starship’s boostback or landing trajectory – basically any maneuver is just a path in 3D space. By
 8
coding this, you’re one step closer to building a full launch simulator. SpaceX uses similar numerical
 integration (just far more complex) to predict where their rockets will land and how to adjust course.
 • 
• 
• 
• 
• 
• 
• 
Day 11 – Focus: Projectile Motion with Drag (Advanced Physics)
 Readings/Videos (1.5+ hrs): Read Briggs Ch. 12.7 on projectile motion in resistive media (about 15
 pages). This section brings together vectors and basic differential equations to account for forces
 like gravity and air drag. It’s dense but highly relevant: pay attention to how drag is modeled
 (proportional to velocity^2, etc.). Complement this with a bit of physics: watch segments of MIT OCW
 8.01 (Classical Mechanics) lectures 3.1–3.4 (~60 min combined) which cover projectile motion,
 including air resistance (“Shooting the Apple” is a classic problem where a monkey drops from a tree
 as a hunter shoots – illustrating gravity’s effect). These will reinforce how to set up equations of
 motion for a flying object. 
Exercises (1 hr): Solve ~6 problems from Briggs 12.7 or similar sources. Key tasks: deriving equations
 of motion with drag, computing how far a projectile goes with a given drag coefficient, etc. For
 instance, a problem might give you a differential equation $dv/dt = -g - (k/m) v^2$ and ask for the
 velocity as a function of time or the terminal velocity. Try one multi-part problem: e.g., “Given a
 rocket launched at X m/s at Y° with drag coefficient C, compute its max height, flight time, range
 using numerical methods or approximations.” This will directly feed into coding. 
Coding (1 hr): Incorporate air drag and thrust into “projectile_sim.py.” This makes your simple
 simulator more realistic:
 ◦ 
◦ 
◦ 
◦ 
◦ 
Define a drag coefficient C_d and cross-sectional area for your rocket (you can assume some
 values, or set C_d ~ 0.3 for a streamlined shape).
 Calculate drag force = ½ * C_d * ρ * A * v^2 (direction opposite velocity). This will need you to
 update acceleration at each step as 
a = (thrust/mass)*direction - g*ẑ - (drag/
 mass)*direction_of_travel . Start simple: maybe assume a constant thrust for a few
 seconds then zero (as a rough model of a rocket burn).
 You might need to reduce time step dt for stability when adding drag. Run the simulation for,
 say, a 1000 kg rocket with a certain thrust for 10 seconds, then coasting.
 Observe how the trajectory differs from the no-drag case: it should not go as high or far due
 to drag.
 This is essentially a basic rocket flight model! It won’t be perfect, but it’s a great
 accomplishment in terms of combining math and code.
 Review/SpaceX Tie-In (30 min): Quiz 4 questions: e.g. definitions (terminal velocity, what factors affect
 drag, etc.), and concept checks (like “Why does a heavier rocket suffer less deceleration from drag (all
 else equal)?”). Tie-in: Relate this to Starship’s re-entry or launch: SpaceX deals with atmospheric
 drag heavily (think of Starship belly-flop maneuver – drag is actually used to slow it down). Note in
 your journal how your simulator could, with further refinement, simulate a Falcon 9 first stage
 trajectory with parachute or grid fins by tweaking drag. Realize that what you built is akin to a
 simplified version of what SpaceX runs in their simulation software to predict landing points.
 Day 12 – Build Day: Refine the Rocket Simulator
 Review & Plan (0.5 hr): Re-read any tricky part of 12.7 or your code where you felt uncertain. Plan what
 improvements or tests you want to do today on the simulator. For example: ensure the code handles
 9
various angles, maybe add output like “did it reach orbit or fall back?” (though reaching orbit is not
 possible in a simple gravity turn sim without enormous speeds, but conceptually).
 • 
• 
• 
• 
• 
• 
• 
Exercises (1 hr): Do 4 mixed vector and motion problems to ensure you’ve got the mechanics down.
 For example: “Compute the resultant of these 3 vectors”, “Given acceleration components, integrate to get
 velocity”, “With drag proportional to v^2, what is the equation for deceleration?”, “How would doubling the
 mass affect a trajectory with drag?”. These reinforce both conceptual and quantitative understanding
 and might hint at tweaks for your sim (like how mass affects things).
 ◦ 
Coding (2 hrs): Polish “projectile_sim.py” into a portfolio-ready Rocket Ascent Simulator:
 Features to add: Perhaps implement both Euler’s method and a more accurate Runge-Kutta
 (RK4) integration for the equations of motion (if you’re comfortable). Compare the results to
 ensure your sim’s accuracy for larger time steps.
 ◦ 
◦ 
◦ 
◦ 
◦ 
◦ 
Allow input of rocket parameters: initial mass, fuel mass, thrust curve (even a simple one:
 constant thrust for T seconds). Maybe incorporate a staging option (two-stage rocket) by
 applying a thrust profile change at a certain time.
 Compute and print out “mission” results: apogee (max altitude), impact distance, etc. If the
 rocket is powerful enough, see if it escapes (in simulation terms, never falls back to ground
 within simulation time).
 Plot the trajectory with clear labels. Possibly plot velocity vs time as well, or altitude vs time.
 Test with a scenario analogous to Starship: e.g., a heavy rocket with high thrust that goes up
 to, say, 10 km and then cuts engines – see how far it travels. Also test a scenario of a weaker
 throw to see the difference.
 Make sure to handle edge cases (like zero thrust = free-fall).
 Time permitting: add an interactive element, or at least clearly separate parameters at the
 top of your script for easy tweaking (so a user/recruiter can play with it).
 Review/SpaceX Tie-In (30 min): Run a full test of your final sim for Week 2. Then write your project
 README (or notes for it): explain what the simulator does and tie it to SpaceX. For example: “Rocket
 Ascent Simulator – This Python tool simulates a rocket’s launch in 3D, including gravity and drag. It can
 model a Falcon 9/Starship-like ascent profile (up to burnout) and predict apogee, range, etc. It uses Euler/
 RK4 integration for the equations of motion. SpaceX tie-in: Demonstrates understanding of rocket flight
 physics (gravity turns, the effect of drag on a booster), which is crucial for launch and landing trajectory
 design.” Also note any ML extension idea (the plan suggests one: maybe tomorrow you’ll integrate
 ML to optimize angle or something).
 Day 13 – ML Integration for Rocket Simulation (Optional)
 Readings/Videos (1 hr): Skim a quick intro on multivariate calculus or matrices if needed (since ML
 may involve understanding multiple inputs). Also, if you haven’t before, read a basic tutorial on
 hyperparameter tuning for Random Forest or XGBoost – since you might use an ML model here.
 Exercises (1 hr): Solve 3 short problems tying math/physics to optimization. E.g., “What launch angle
 maximizes range for a projectile without drag? (45°) With drag? (a bit lower, maybe ~40° depending on
 drag).” Or “How does varying coefficient of drag affect max altitude?” Think how you’d formalize these as
 a data-driven problem (angle in, outcome out).
 Coding (1.5 hrs): Use your rocket simulator data to apply ML. One idea:
 ◦ 
◦ 
Run your simulator for various launch angles (say 5° increments from 5° to 85°) and record
 the range or max altitude achieved.
 Use this dataset to train a simple Random Forest or even just analyze to find the optimal
 angle under drag (it won’t be exactly 45° because drag skews it).
 10
◦ 
◦ 
• 
Alternatively, vary another parameter (like initial velocity or drag coefficient) and try to predict
 outcome.
 The ML part can be very simple – even a polynomial fit would do, but since you know ML, a
 quick RandomForestRegressor to predict, say, range given angle might be cool. The point is
 to show you can loop over simulations to create data and then use ML to glean insights
 (something SpaceX might do for design trade studies).
 Review/SpaceX Tie-In (30 min): Reflect on how real-time adjustments or optimization in rockets could
 use ML. For example, SpaceX might use machine learning to fine-tune landing trajectories or to
 quickly evaluate thousands of simulations of different conditions (Monte Carlo simulations with ML
 surrogates). Write down: “Using ML on my rocket sim mimics how SpaceX could optimize launch
 parameters for maximum range or safe landing – essentially automating what I just did manually.” Save a
 plot of angle vs range (with and without drag) as this visual might be a neat addition to your project
 documentation.
 • 
• 
• 
• 
• 
• 
Day 14 – Week 2 Review and Portfolio Polish
 Review (0.5 hr): Summarize the key vector and motion concepts learned (dot/cross product, vector
 functions, projectile motion with/without drag). Ensure you can explain in simple terms how a
 rocket’s 3D trajectory is computed and what factors (like drag) do to it.
 Week 2 Quiz (1 hr): Take a 10-question quiz you design, covering vectors (concepts and calculations),
 basic kinematics, and one simple drag calculation. This ensures you can still do the math by hand for
 interview situations (SpaceX interviews might throw fundamental physics questions).
 Project Demo (1 hr): Record a short demo of your Rocket Ascent Simulator. Show the simulation
 running with a certain set of parameters (perhaps compare two runs: one with a high launch angle,
 one shallow, or one with high drag vs low drag). Narrate what’s happening (“Here the rocket has a
 higher drag coefficient, you can see it doesn’t go as far…”). If possible, display the trajectory plot in
 the video. Keep it ~2 minutes.
 ◦ 
◦ 
Portfolio Upload & GitHub (1 hr): Push your finalized code to GitHub under a repository (maybe reuse 
“rocket-basics” repo or make a new one like “rocket-ascent-sim”). Include:
 A README with overview, instructions to run, sample results, and SpaceX relevance (e.g. “This
 sim is a basic prototype of how one might simulate a Falcon 9 or Starship first stage trajectory.”).
 Any images (plots) or data files if useful.
 ◦ 
◦ 
Possibly link to the demo video (you could upload it unlisted to YouTube or just mention you
 have it).
 Module 1 Wrap-Up: Congratulations, you’ve completed Module 1! By now you have two solid projects:
 Project 1: Rocket Ascent Simulator (3D motion with drag, plus an ML angle optimizer
 extension).
 ◦ 
Project 2: Conic Orbit Visualizer (plots orbital trajectories and ties to mission profiles).
 Both are on GitHub with README and demo, making you highly visible to recruiters
 searching for hands-on aerospace projects. In your journal, reflect on the past 8 weeks of
 foundations – it’s a big chunk of work. Note any topics you struggled with to possibly revisit
 later. Finally, do a fun reward: maybe watch a full replay of a SpaceX launch and actually
 understand the announcer when they talk about “trajectory nominal” or “apogee” now that
 you’ve simulated those concepts yourself. When ready, gear up for Module 2!
 11
Module 2: Orbital Mechanics and Mission Design (8 Weeks) – 
Satellites, Transfers, and Starship Missions
 Module Overview: Now that you have the fundamental math/physics down, Module 2 dives into classical
 orbital mechanics – essentially applying those conic sections and calculus concepts to real-world orbits and
 maneuvers. The focus is on Earth orbits, interplanetary transfers, and rendezvous, which are directly
 relevant to SpaceX’s satellite operations (Starlink constellation) and Starship’s mission profiles. You’ll work
 with actual orbital data and tools, and complete two major projects: - Project 1: “Starlink Orbit
 Propagator” – using real satellite Two-Line Element (TLE) data to propagate orbits (with perturbations like
 Earth’s oblateness and atmospheric drag) and predict how a satellite’s orbit decays over time. You’ll
 integrate an SGP4 algorithm and even apply an ML model (e.g. XGBoost) to forecast satellite lifespan or re
entry date. - Project 2: “Starship Trajectory Planner” – a tool to compute interplanetary transfer orbits
 (like Hohmann transfers to Mars) and perform basic rendezvous calculations (using Clohessy-Wiltshire
 equations for orbital rendezvous). This showcases your astrodynamics savvy by calculating delta-V
 requirements for missions and perhaps simulating a refueling orbit meeting – critical for Starship’s
 envisioned Earth-orbit refueling and Mars missions.
 By the end of Module 2, you’ll not only have those two projects on GitHub, but also a stronger grasp of the
 orbital mechanics theory behind them. SpaceX Tie-in: This module aligns with SpaceX’s core operations 
from managing the Starlink constellation (tens of thousands of satellites orbiting Earth) to planning
 Starship’s complex journeys beyond Earth. SpaceX recruiters will love that you’ve worked with real orbital
 data and can discuss things like rendezvous or orbital decay with confidence.
 3
 Resources & Tools for Module 2: In addition to textbooks and videos, you’ll start using professional tools: 
NASA’s GMAT (General Mission Analysis Tool) – a free, open-source astrodynamics tool. Install this in
 Week 1 of the module. You can use GMAT to double-check your orbital calculations or simulate scenarios
 (e.g., verify that your Hohmann transfer calculations match GMAT’s output ). This adds credibility to your
 work – showing you can use the same tools aerospace companies use. - STK (Systems Tool Kit by AGI) – a
 powerful orbit visualization software (free student version). It’s optional but highly recommended for
 visualization. For example, after coding your Starlink propagator, you can use STK to create a slick 3D
 animation of the satellite orbits and ground tracks. This makes for great visuals in your portfolio. 
Celestrak & TLE data – You’ll be pulling real TLE (Two-Line Element) files for Starlink satellites from
 celestrak.com or Space-Track. This introduces you to handling real orbital data. - Online Courses/Certs: As
 part of this module, consider completing the NASA “Orbital Mechanics” Pathways online course (free) 
it’s a basic intro to orbits and could provide a certificate for your resume. Allocate about 2 weeks part-time
 for this, possibly overlapping with your study plan below.
 Week 1-2: Orbital Mechanics Fundamentals and Certification
 • 
• 
• 
Week 1 – Orbital Basics & Frames: Focus on understanding how orbits are described and
 measured.
 Topics: Kepler’s laws, orbital elements (semi-major axis, eccentricity, inclination, etc.), energy and
 period of orbits, reference frames (geocentric, heliocentric, inertial vs rotating).
 Readings: An orbital mechanics textbook or NASA’s online material on “Orbit Determination 101”. If
 you have the classic “Orbital Mechanics for Engineering Students” or SMAD (Space Mission Analysis and
 12
Design), read the chapters on two-body orbits and Kepler’s laws. Alternatively, the NASA Pathways
 module will cover these basics.
 • 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
Exercises: Calculate orbital period from semi-major axis (e.g., given a = 7000 km for a LEO satellite,
 what’s the period?). Convert between orbital elements and state vectors (position/velocity) for simple
 cases (circular or equatorial orbits). These are pen-and-paper or spreadsheet calculations to get
 comfortable with the numbers.
 ◦ 
Hands-on: Install GMAT and STK this week. Follow a simple tutorial for each:
 In GMAT: replicate an example (like launching a satellite into a circular orbit and propagating
 for one day).
 ◦ 
In STK: create a scenario with one satellite in LEO. Play with the 3D view and generate an
 orbital report (STK can output orbital elements over time).
 Project integration: Start a new GitHub repo “starlink-propagator”. Write a README introduction.
 You won’t code much yet, but set up the structure (maybe a Python script that can read a TLE).
 Ensure you have the SGP4 library ready (e.g., install 
sgp4 Python package).
 Certification: Begin the NASA Pathways Orbital Mechanics course if you choose. Complete the first
 module which likely covers similar basics. 
SpaceX Tie-In: Recognize that every Starlink satellite operates under these orbital principles. Write a
 note: “Knowing how to compute an orbit’s period or when a satellite will pass over a ground station is
 exactly what I’d do at SpaceX when working on Starlink.”
 Week 2 – Perturbations & Orbital Maneuvers Basics: Now that two-body (ideal) orbits are
 understood, look at what perturbs real orbits and how we change orbits intentionally.
 Topics: Perturbations like Earth’s oblateness (J2 effect causing the Right Ascension of Ascending Node
 (RAAN) to drift), atmospheric drag (causing orbital decay in low orbits), and an intro to orbital
 maneuvers (delta-V, Hohmann transfer concept).
 Readings: Sections from SMAD or an astrodynamics source on perturbations (J2 effect) and drag.
 NASA’s “Orbital Debris” or similar resources might have short descriptions of decay. Also read about
 Hohmann transfers (the classic two-burn transfer between two circular orbits) – plenty of online
 explainers exist.
 Exercises: Compute a simple perturbation: e.g., use the formula for J2-induced RAAN drift to estimate
 how much a 53° inclination LEO (Starlink orbit) node drifts per day. Calculate roughly how long it
 takes a satellite at 550 km to re-enter due to drag (you can use a simplified exponential atmosphere
 model). Also, practice delta-V calculations: how much delta-V to raise a circular orbit from 300 km to
 550 km? (This is roughly what a Starlink satellite might do after deployment).
 Hands-on: Use GMAT to simulate a perturbation: e.g., propagate a 550 km orbit for a month with J2
 on vs off, and see the difference in RAAN. Use STK to visualize a ground track of an orbit over a day 
see how Earth’s rotation and orbit combine. These tools will solidify concepts (and you can
 screenshot results for your notes/portfolio).
 Project work: Start coding the Starlink Propagator:
 ◦ 
◦ 
◦ 
Use the SGP4 Python library to propagate a real Starlink TLE. (Find a recent TLE for a Starlink
 satellite on Celestrak – they’re usually under “Starlink”.) Write a script to read the TLE and
 propagate the satellite’s position over, say, one week with a time step of 60 seconds.
 Incorporate simple perturbation models: after using SGP4 (which already includes J2 and
 other models internally), maybe also propagate with a simple drag model by manually
 tweaking the semi-major axis over time.
 Output the predicted orbital decay: e.g., how altitude changes over the week.
 13
◦ 
• 
If you can, compare your propagation to another source (maybe STK or Celestrak’s
 predictions) to verify accuracy.
 Certification: Continue the NASA course – by end of Week 2 you might finish it and get a certificate.
 Add that to your resume (and LinkedIn) when done!
 • 
SpaceX Tie-In: By now you’ve actually handled real Starlink data. In your notes, describe how SpaceX
 might use such propagation: “Starlink engineers must predict when and where to deorbit old satellites.
 My tool emulates that process, using real orbital elements.” This is a huge credibility boost – you’re not
 just doing textbook work, you’re using real data, which SpaceX values in candidates.
 Week 3-4: Advanced Orbits, Starlink Constellation & Project 1 Completion
 • 
• 
• 
• 
• 
• 
Week 3 – Starlink Constellation & Ground Tracks: Expand your understanding to constellation
 design and specifics of Starlink.
 Topics: Learn what a Walker constellation is (common method to arrange satellite orbits for full
 Earth coverage) and how Starlink is organized (multiple shells of orbits at different inclinations).
 Study ground track patterns and revisit coordinate systems (geographic coordinates vs orbital
 coordinates).
 Readings: White papers or blog posts on Starlink’s constellation (e.g., how many planes, how
 satellites hand off coverage). Also, read about ground tracks in an astrodynamics text – how to
 calculate revisit times and coverage.
 Exercises: Compute something like: given X satellites evenly spaced in Y planes, what’s the spacing in
 RAAN and true anomaly? Or, given an orbital period, how many orbits per day and thus how ground
 track repeats. If Starlink has 72 orbital planes, what’s the RAAN separation? These are more
 conceptual calculations but show you grasp constellation geometry.
 Hands-on: If you have STK, try loading a simple constellation scenario (STK might have templates).
 Even without STK, you can script a small Python calculation to generate a set of satellite orbits and
 maybe visualize some coverage pattern (e.g., using matplotlib basemap or just outputting lat/long
 positions).
 Project work: Finalize Project 1: Starlink Propagator:
 ◦ 
◦ 
◦ 
◦ 
◦ 
◦ 
Make sure your script can propagate multiple satellites (perhaps take 5 TLEs from one Starlink
 plane).
 Add a feature to compute and plot RAAN drift over time for these satellites (J2 effect causes
 RAAN of lower orbit satellites to change – Starlink satellites in same plane should maintain
 RAAN, whereas different inclinations have different node drift).
 Add atmospheric drag modeling: perhaps allow user to input a solar activity level (high/low)
 and adjust decay rate.
 ML integration: Train a simple XGBoost (or Random Forest) model on historical data or
 simulated data to predict satellite decay time. For example, create a dataset: inputs = initial
 altitude, inclination, solar activity; output = time to deorbit. If you don’t have real data,
 simulate a bunch with your propagator by varying parameters and seeing when altitude
 drops below 300 km. Train the model on that. Then you can ask it, “If I launch a satellite at
 550 km in high solar activity, how long will it last?” – the ML will predict based on patterns.
 This showcases your ML skills in a space context.
 Write results to a file or plot them: e.g., a graph of altitude vs time for a sample satellite, or a
 bar chart of predicted lifespans under different conditions.
 Ensure the code is cleaned up, with functions (maybe one for propagation, one for applying
 drag, etc.).
 14
• 
Testing: Validate your propagator against known figures: e.g., a Starlink at 550 km typically deorbits
 in ~5 years after failure (just a rough figure). Does your model give a similar order of magnitude? If
 yes, great.
 • 
• 
• 
• 
• 
• 
• 
• 
Documentation: Draft the README for this project, explaining how to use it and what each feature
 does.
 SpaceX Tie-In: Emphasize in documentation: “This tool uses real Starlink TLE orbital data to simulate
 orbit trajectories and decay – akin to what SpaceX’s orbital engineers do to manage the constellation.”
 Also mention how you integrated ML (SpaceX loves autonomy and intelligent systems). By the end of
 Week 3, Project 1 should be essentially done and ready to showcase.
 Week 4 – Hohmann Transfers & Delta-V (Start Project 2): Shift focus to orbital maneuvers and
 mission design, which feeds into your Starship trajectory planner.
 Topics: Hohmann transfer orbits (the most fuel-efficient two-impulse transfer between two circular
 orbits), Lambert’s problem basics (finding an orbit that goes from point A to B in a given time 
underpinning rendezvous calculations), and basics of interplanetary transfers (phasing, launch
 windows).
 Readings: Read up on Hohmann transfers (plenty of online sources or textbook chapters). Learn the
 formula for Hohmann transfer delta-Vs. Also read about Clohessy-Wiltshire (CW) equations, which
 describe relative motion in orbit – these are used for spacecraft rendezvous (like how Dragon meets
 the ISS, or how Starship will rendezvous for refueling). A resource could be NASAs Rendezvous and
 Proximity Operations primer or an astrodynamics text for CW equations.
 Exercises: Calculate a few key figures: delta-V for a Hohmann transfer from LEO to GEO (approx 4 km/
 s), delta-V for Earth to Mars Hohmann (about 3.5 km/s from LEO, but more from ground). Also
 practice using CW equations: e.g., if two spacecraft are 10 km apart in the same orbit, how long until
 they meet if one has a slight velocity difference? Do one rendezvous problem calculation by hand to
 get a sense.
 Project work: Start Project 2: Starship Hohmann/Lambert Tool:
 ◦ 
◦ 
◦ 
◦ 
◦ 
Write a script or Jupyter notebook where given two orbits (e.g., Earth parking orbit and Mars
 transfer orbit), you compute transfer parameters. Start with a simple Hohmann: input radii of
 two circular orbits, output the delta-V for each burn and transfer time.
 Extend to interplanetary: Earth to Mars – you’ll need orbital radii and perhaps adjust for Mars
 not being coplanar or requiring plane change (you can simplify by assuming coplanar).
 Implement Lambert’s problem (this is advanced; if too much, skip detailed Lambert solver
 and use a simpler approach): given two positions (e.g., Earth position at departure and Mars
 position at arrival) and time of flight, solve for the transfer orbit. There are Python libraries
 (like poliastro) that can solve Lambert’s problem – feel free to use one for the heavy lifting
 while understanding conceptually what it’s doing.
 Implement CW equations for a simple rendezvous: say you have a target in circular orbit and
 a chaser slightly behind – compute the relative motion and perhaps the velocity the chaser
 needs to close the gap in a certain time.
 Interface: Make the tool interactive: perhaps it asks, “Mission: Earth to Mars or LEO
 rendezvous?” and then proceeds accordingly.
 SpaceX Tie-In: Realize you’re coding what SpaceX mission planners do. Starship’s orbital refueling
 will require rendezvous in Earth orbit – that’s CW equations at work. Starship’s Mars travel needs
 Hohmann transfers. Jot down: “This tool is basically a simplified mission design software. SpaceX likely
 15
uses more complex versions (and tools like GMAT), but the principles are the same. I’m demonstrating I can
 calculate and plan these trajectories.”
 Week 5-6: Complete Starship Mission Planning Tool and Integration
 • 
• 
• 
• 
• 
• 
• 
• 
Week 5 – Finish Project 2 and Integrate Tools: This week, finalize the Starship trajectory planning
 project and validate it with professional tools and data.
 ◦ 
Coding Project 2: Complete all features:
 Ensure your Hohmann calculator works for various inputs (maybe allow user to input any two
 altitudes).
 ◦ 
◦ 
◦ 
◦ 
Ensure your Lambert solver (if implemented or via library) can output a feasible trajectory. For
 instance, pick a known Earth-Mars transfer window date and see if it gives a reasonable delta
V. (Using 
poliastro with actual ephemeris would be great, but if not, you can assume
 circular orbits.)
 Implement an output that prints the results in a nice format: e.g., “Hohmann Transfer: Burn1 =
 X m/s, Burn2 = Y m/s, TOF = Z days, Total ΔV = ...” and “Rendezvous: relative velocity needed = ...”,
 etc.
 Add a small ML angle: maybe use your Random Forest skill to optimize something like launch
 timing. For example, train a model (or simply brute-force compute) to see how varying
 departure date affects the required delta-V to Mars (which it does due to planetary
 alignment). An ML model could interpolate these results so you can quickly estimate the best
 launch window.
 Include a feature to output a suggested launch window for least delta-V (even if
 approximate).
 Validation: Use GMAT to validate one of your results. For example, set up an Earth-to-Mars transfer in
 GMAT for the same dates and see if the delta-V matches your tool’s output within reason. Or
 simulate a rendezvous in GMAT. This step isn’t required, but if done, mention it as validation (shows
 thoroughness).
 Documentation: Write the README for Project 2. Emphasize SpaceX use cases: “This tool can be used to
 plan a Starship refueling mission in orbit or a trajectory to Mars. For example, it calculates ~* m/s for a
 Hohmann transfer to Mars which aligns with known mission profiles.” If you used any library like
 poliastro, note that and that you understand the underlying physics.
 Portfolio: Make sure Project 2 is on GitHub with proper structure. Perhaps include a sample JSON or
 text file of example outputs, or a chart (like porkchop plot if you got fancy with transfers).
 Exercises/Review: As you wrap up, do a quick review of orbital mechanics basics. Maybe take a practice
 quiz from the NASA course or textbook questions to ensure you can explain things like “what is a
 Hohmann transfer?” or “how do you change the inclination of an orbit?” clearly – these are things
 SpaceX might ask in interviews for relevant roles.
 Week 6 – Module 2 Review & Showcase: Use this week to consolidate everything from Module 2
 and ensure both projects are polished and visible.
 ◦ 
Testing & Results: Run both Project 1 and Project 2 tools for a “showcase scenario”:
 For Project 1 (Starlink Propagator): pick a particular Starlink satellite and propagate it 6
 months into the future with your tool. Show how its orbit decays a little. Also use your ML to
 predict lifetime. Save a plot of altitude over time.
 16
◦ 
◦ 
• 
• 
For Project 2 (Starship Planner): simulate a mission – e.g., “Starship to Mars in 2027”. Output
 the delta-V, time of flight, etc., and maybe an optimal launch date. Also simulate a Starship
 rendezvous with another in orbit (e.g., refueling) – even if just conceptual.
 These examples can be part of your portfolio (in the README or as separate reports).
 Demo Videos: Record short videos (1-2 minutes each) for Project 1 and Project 2, if possible. Show the
 usage and outputs, and perhaps your plots. Narrate enthusiastically, as if presenting to a hiring
 manager: highlight that you used real data and that these tools solve real aerospace problems.
 LinkedIn/Networking: By now you have four solid projects (Module 1’s two and Module 2’s two).
 Update your LinkedIn to list these projects under a section “Space Systems Projects”. You can even
 make a post about completing Module 2, sharing a cool graphic from your work (maybe an
 animation of satellite orbits or a plot of a Mars transfer). This is where networking starts paying off 
people might notice and engage.
 • 
• 
Week 6 Review: Take a comprehensive quiz or do a mock interview with yourself covering Modules 1-2
 content (foundation + orbital mechanics). Questions could range from “Explain what an eigenvector
 is” to “How do satellites maintain their orbits?” to “What’s a PID controller?” (just in case – SpaceX
 might throw in controls questions too). Identify any weak spots to revisit in later modules.
 Celebrate: Module 2 was intense and deeply technical – congratulate yourself! You’ve essentially
 covered an entire Orbital Mechanics course and built real software that few students ever do on their
 own. Enjoy a weekend off or a fun activity (maybe try Kerbal Space Program if you haven’t already,
 to celebrate – see if you can reenact your Earth-Mars transfer in game!).
 Module 3: Space Systems & Propulsion Engineering (8 Weeks) – 
Designing Rockets and Constellations
 Module Overview: With the fundamentals and orbital mechanics in your toolkit, Module 3 moves to Space
 Systems Engineering – understanding how all the pieces (structures, propulsion, payload, etc.) come
 together in a spacecraft or launch system. You’ll delve into rocket propulsion basics, mass budgets, and
 trade studies (e.g., how adding weight in one subsystem affects performance). You’ll also learn about
 designing satellite constellations and space mission architecture. This module’s projects are: - Project 1:
 “Starship Subsystem Trade Simulator” – a simple tool to simulate how changes in rocket design affect
 performance. For example, altering engine count, propellant mass, or structural mass and seeing the
 impact on delta-V and payload. You might base this on the Tsiolkovsky rocket equation and staging
 equations from SMAD Ch. 11. The goal is to show you can do systems trade-offs like reusability vs. payload.- Project 2: “Constellation Designer” – a program to help design and analyze a satellite constellation (like
 Starlink). Input parameters like number of satellites, orbit altitude, inclination, and the tool outputs
 coverage properties: revisit time, coverage gaps, ground track visuals. This leverages both your orbital
 mechanics knowledge and computational skills.
 By the end of Module 3, you will have a good grasp of how rockets are designed (at a high level) and how
 large-scale systems like constellations are planned – plus two more portfolio projects that demonstrate
 systems thinking. SpaceX tie-ins: This module aligns with things like Starship’s engineering (balancing huge
 rockets’ mass and engines for reusability) and Starlink’s network design (global coverage optimization).
 SpaceX hiring managers appreciate candidates who can zoom out and consider entire systems, not just
 isolated equations.
 17
Key Resources for Module 3: - SMAD (Space Mission Analysis and Design) – This is a great reference for
 system engineering concepts like mass budgeting, delta-V budgeting, constellation design basics, etc.
 Chapter 11 in particular deals with launch vehicle performance and staging. - Rocket Propulsion by Sutton – a
 classic text on rocket engines. You might not read it fully, but Chapter 3-4 cover engine performance
 (specific impulse, thrust equations) which is useful for Project 1. - Online tools: Consider using spreadsheets
 or MATLAB for quick calculations (sometimes easier for trade studies). But Python can do too. - KSP as Lab: If
 you have Kerbal Space Program, it’s a great “lab” for Module 3. You can virtually test how adding weight or
 changing engines alters a rocket’s ability to reach orbit, reinforcing the concepts you calculate.
 Weeks 1-2: Rocket Propulsion & Mass Budgeting
 • 
• 
• 
• 
• 
• 
• 
• 
• 
• 
Week 1 – Rocket Propulsion Fundamentals:
 Topics: Thrust, Specific Impulse (Isp), the Rocket Equation ($\Delta V = I_{sp} g_0 \ln(m_0/m_f)$),
 staging benefits. Basic thermodynamics of engines (optional deeper dive if interested).
 Readings: Read relevant sections of Sutton’s Rocket Propulsion Elements (Ch. 2 or 3 on rocket
 performance), or a summary online of rocket equation derivation and usage. SMAD Ch. 11 (Launch
 Vehicles) is a goldmine for simplified analysis of multi-stage rockets – read the parts on staging and
 payload fraction.
 Exercises: Calculate a few rocket equation examples: e.g., If Starship’s dry mass is X and prop mass is
 Y with Isp ~380 s, what’s the theoretical delta-V? How does that compare to what’s needed for orbit
 (~9400 m/s)? Calculate how staging improves performance: e.g., do a 2-stage rocket with given
 parameters and see total delta-V.
 Project 1 work: Start the Starship Subsystem Trade Simulator:
 ◦ 
◦ 
◦ 
Define a baseline rocket (maybe use Starship + Super Heavy as a template: Stage1 mass,
 Stage2 mass, Isps, etc.). Collect approximate data: Starship dry ~120t, prop ~1000t, Isp ~380s;
 SuperHeavy dry ~200t, prop ~2700t, Isp ~330s (vacuum values rough).
 Write code that calculates delta-V given these inputs using rocket equation for two stages.
 Make sure it matches known figures (~Starship+SuperHeavy ~> 12000 m/s possible).
 Plan what trades to simulate: e.g., vary engine count (which affects dry mass and maybe Isp),
 vary structural mass fraction, etc.
 SpaceX Tie-In: Consider SpaceX’s trade-offs: Starship is fully reusable, which costs some payload.
 Note: Elon Musk often talks about mass ratios. Write down: “Understanding rocket equation helps
 explain why reusability (adding landing propellant, heat shield weight) lowers payload. I can quantify
 these effects now.”
 Week 2 – Mass Budgeting & Systems Engineering:
 Topics: Mass breakdown of a spacecraft (structure, propulsion, payload, avionics, etc.), margin and
 contingency, optimization between subsystems. Basics of systems engineering: requirements and
 trade studies.
 Readings: SMAD’s sections on mass estimation (usually they have tables of typical percentage mass
 for each subsystem). Also read about how adding payload or fuel affects launch vehicle performance
 (there are likely case studies, e.g., how Falcon 9 evolved with more thrust to carry Starlink satellites).
 Exercises: Try a trade study on paper: e.g., if you increase payload by 10%, how much more propellant
 is needed to reach the same delta-V? Or if you improve engine Isp by 5%, how much more payload
 can you carry? These give a feel for sensitivities.
 18
• 
• 
• 
◦ 
Project 1 work: Continue building the Trade Simulator:
 Implement ability to adjust one parameter at a time and compute outcomes. For example, a
 function 
simulate_vehicle(stage1_propellant, stage2_propellant, stage1_dry, 
◦ 
◦ 
◦ 
◦ 
stage2_dry, Isp1, Isp2) that returns total $\Delta V and payload fraction.
 Create a loop or interface to do studies: e.g., vary Stage 2 dry mass from 100t to 150t in steps,
 and see how delta-V drops. Or vary Isp.
 Possibly integrate an optimization: for example, you could use a simple search to find the
 optimal staging (mass split between stages for maximum delta-V).
 If comfortable, incorporate an ML element: maybe train a quick model to predict payload
 capacity given input parameters – but this might be overkill since the rocket equation is
 analytic. Alternatively, use ML for a different angle: classify whether a given design can reach
 orbit or not (0/1).
 Start thinking about output: maybe plots of delta-V vs some parameter, or a 3D plot of
 payload vs stage1&2 prop mass.
 Testing: Compare your simulator’s output to known rockets: e.g., input Falcon 9 values (approx) and
 see if it shows ~some payload to LEO. Or try a single-stage to orbit scenario to see how unrealistic it
 is (which will show why staging is needed).
 SpaceX Tie-In: Journal how this is exactly what SpaceX engineers do early in design – run
 spreadsheets and sims to decide vehicle specs. For instance: “Through this simulator, I can explore
 questions like ‘What if Starship had 9 engines instead of 6? How would that affect mass and delta-V?’ which
 is similar to the real trade studies SpaceX did when designing Raptor engines and Starship’s structure.”
 Weeks 3-4: Complete Trade Simulator & Constellation Design Basics
 • 
• 
• 
• 
• 
Week 3 – Finalize Project 1 (Trade Simulator) and Analyze Results:
 Project 1 coding: Finalize features:
 ◦ 
◦ 
◦ 
◦ 
◦ 
Include multiple trade options: maybe a menu to choose what to vary (propellant mass,
 engine Isp, etc.).
 Ensure it can calculate payload to orbit: incorporate a criterion like “reaches orbit if delta-V >
 9400 m/s” and output yes/no or payload margin.
 Add real-world comparison mode: allow inputting parameters of known rockets (Saturn V,
 Falcon Heavy, etc.) and output their delta-V to show your tool works.
 Make the output user-friendly: for example, print a table of scenarios or generate a
 matplotlib plot (e.g. “Payload vs Stage 2 Dry Mass” curve).
 If ML was added, incorporate that output too (though it might be simpler to stick to
 analytical).
 Documentation: Write the README for Project 1. Explain the assumptions (two-stage, no gravity drag
 losses considered, etc.). Provide a couple of example studies: e.g., “Simulation shows that increasing
 Stage 2 dry mass by 20t (for additional heat shielding in a reusable design) would reduce payload by X%.
 This quantifies the cost of reusability.” Such insights directly mirror what SpaceX weighs (trade-off
 between adding heat shield vs losing payload).
 Testing: Use the simulator to answer a cool question: “Could a single-stage Starship reach orbit if made
 of carbon fiber and high performance engines?” (Just a hypothetical fun test – likely answer is still no,
 but you can show the delta-V shortfall). Or “What if Starship had no reuse (expended), how much more
 payload?” – maybe it gains 20%, etc.
 Wrap-up Project 1: Ensure the code and documentation are on GitHub. Consider recording a short
 demo video showing you tweaking a parameter and the tool responding.
 19
• 
• 
• 
• 
• 
• 
• 
• 
Exercises: Do a quick review of rocket performance concepts (maybe a few quiz Qs like “Why is
 staging beneficial?” or “Define specific impulse.”). Make sure you can articulate these, as they might
 come up in interviews.
 SpaceX Tie-In: You’ve basically created a mini-Monte Carlo simulation that SpaceX might use in early
 design. Write a reflection: “This project taught me how sensitive rocket design is. I see why SpaceX chose
 stainless steel for Starship despite weight penalty – my sim shows small weight changes can be offset by
 other factors like cheap fueling and refueling.” This kind of holistic understanding is impressive to
 share.
 Week 4 – Satellite Constellation Design Fundamentals:
 Topics: Coverage analysis – how many satellites to cover the Earth, what altitude gives what footprint,
 inclination effects on coverage at different latitudes. Also introduction to communication constraints
 (latency vs altitude, etc.), though that might be more detail than needed.
 Readings: SMAD has chapters on communications and constellations. Focus on the concept of a 
Walker constellation (defined by parameters: number of planes, satellites per plane, phasing). Also
 read any case study on Iridium or GPS constellations for context (Starlink info too).
 Exercises: Basic calculations: for a given altitude, what’s the ground coverage diameter (using simple
 geometry, Earth central angle = 2 * acos(R_e/(R_e+h))). How many satellites at that altitude to cover
 the Earth if evenly spaced? If inclined at 53°, what latitudes aren’t covered? These rough calcs build
 intuition.
 ◦ 
Project 2 start: Begin Constellation Designer tool:
 Decide on scope: maybe focus on ground coverage and revisit times.
 ◦ 
◦ 
◦ 
◦ 
◦ 
Initial feature: given number of satellites, altitude, inclination, distribute satellites and
 compute coverage gap at equator vs poles.
 You might simplify Earth as sphere and assume each satellite covers a certain circular area on
 ground (half-angle = elevation angle of say 30° minimum for coverage).
 Or more dynamically, for a given point on Earth, calculate how often a satellite passes
 overhead given certain constellation (revisit time).
 Use Python (and possibly libraries like 
numpy and maybe 
skyfield or 
again) to generate satellite positions over time and check coverage.
 poliastro
 Start with simpler: one orbit’s ground track – compute how long until it comes over same
 point (ground track repeat period).
 ◦ 
If visualization is feasible, try to plot ground tracks for a few orbits.
 SpaceX Tie-In: Starlink is the obvious connection. Note: Starlink has ~550 km altitude, 53° (and other
 shells 70° inclination, etc.). Understand why (53° covers most populated areas, multiple shells for
 polar). Plan to incorporate Starlink as an example in your tool (like a preset configuration to analyze).
 Weeks 5-6: Complete Constellation Tool and Module 3 Wrap-Up
 • 
• 
Week 5 – Complete Project 2 (Constellation Designer):
 Project work: Finalize features:
 ◦ 
◦ 
Allow input: number of orbital planes, satellites per plane, inclination, altitude.
 Compute coverage: one approach – calculate the maximum gap in longitude at equator
 between adjacent satellites’ ground tracks. Or simulate one day and find longest gap for a
 given latitude.
 20
◦ 
◦ 
◦ 
◦ 
◦ 
• 
Compute revisit time: how often does a satellite pass over a given point (especially important
 for higher latitudes if fewer satellites).
 If ambitious, incorporate a simple optimization: for instance, given a desired maximum gap,
 suggest how many satellites are needed.
 Provide output metrics like: coverage percentage, maximum gap in minutes, average revisit
 time globally.
 Possibly integrate ML if applicable: maybe train a model to predict coverage from
 constellation parameters (though an analytical approach might suffice).
 Add visual output: e.g., a world map with ground tracks or satellite positions (if coding that
 isn’t too time-consuming – libraries like Basemap or cartopy could help).
 Testing: Use your tool on known constellations:
 ◦ 
◦ 
◦ 
• 
• 
e.g., GPS: 24 satellites, 55° inclination ~20k km altitude – does your tool show full coverage
 with ~6 satellites in view? (GPS ensures 4+ always).
 Starlink example: does your tool estimate that ~1584 sats at 550 km/53° gives near global
 coverage? (It should show some gap at extreme poles).
 If you find any known stat (like “Starlink ensures every point sees a sat at least every X
 minutes”), see if your output aligns.
 Documentation: Write README for Project 2. Explain concepts like what input parameters mean.
 Provide an example analysis (like “Using the tool for Starlink’s first shell: result – coverage gap at
 poles ~XX minutes, which matches expectations”). This will impress that you validated your tool.
 Demo: Record a video of using the Constellation Designer – maybe screen-record running it for a
 scenario and narrate the output (especially if you have a cool visual or chart).
 • 
• 
• 
• 
• 
• 
SpaceX Tie-In: Emphasize in documentation that this addresses Starlink global internet optimization.
 Perhaps mention: “This tool can assist in designing constellations like Starlink – for instance, determining
 how adding satellites improves coverage. SpaceX can use such analysis to decide how many satellites to
 deploy for continuous coverage.”
 Week 6 – Module 3 Review and Portfolio Polish:
 Review: Summarize what you learned about rocket design and constellation planning. Ensure you can
 articulate a coherent story of how an idea goes from concept to a full system. For instance, practice
 explaining “How does Starship’s design enable its mission of Mars colonization?” touching on
 reusability, payload, etc., or “How does Starlink architecture ensure low latency coverage?”
 Complete any certifications: If you opted for an edX course like “Intro to Aerospace Engineering (TU
 Delft)”, try to wrap it up around now. It will reinforce some of these concepts and you’ll have another
 certificate for your resume.
 Portfolio check: By now, you have 6 projects (2 per module for first 3 modules). That’s substantial!
 Make sure each GitHub repo is polished:
 ◦ 
◦ 
◦ 
◦ 
Repos have descriptive names and README files (with SpaceX context noted).
 Code is pushed and well-commented.
 Include any license if you want (MIT license, etc. not crucial but professional).
 Consider creating a portfolio page (maybe a simple GitHub Pages site or a Notion page)
 listing all projects with links, descriptions, and demo videos. This can be the link you send to
 recruiters.
 Networking: Leverage AIAA or other networks: share your progress, ask for feedback. Perhaps post
 one of your project demos on a forum (Reddit r/SpaceX or r/aerospace) to get comments 
sometimes industry folks hang out there.
 21
• 
• 
Quiz: Do a 10-question cumulative quiz (covering Modules 1–3 topics). This is a midpoint check that
 you’re retaining info.
 Next Steps: Module 4 will veer into human factors and policy – a change of pace. Before moving on,
 list any pending questions you have from Modules 1–3 that you might want to research later (e.g.,
 you learned basics of rocket equation but maybe want to learn more about engine cycles; or you did
 constellation geometry but might later revisit link budget calcs). This list ensures you remember to
 deepen knowledge where needed, perhaps in Module 6 (Electives).
 Celebrate finishing Module 3 – you’ve built an impressive portfolio so far and covered a lot of engineering
 ground! Take a moment to acknowledge that you effectively self-taught an aerospace engineering core
 triad (fundamentals, orbits, systems) and created tangible results. SpaceX will value that persistence and
 breadth.
 Module 4: Human Factors, Regulations, and Space Policy (6 Weeks)– Beyond Engineering: Ensuring Mission Success
 Module Overview: Engineering doesn’t happen in a vacuum – especially at SpaceX, where missions involve
 human passengers (Crew Dragon, future Starship crews) and navigating complex regulatory landscapes
 (launch licenses, satellite spectrum, space debris rules). Module 4 covers the “softer” but crucial aspects:
 human factors (how to keep astronauts safe and comfortable) and space policy/regulation (legal, safety
 standards, orbital debris mitigation). These areas might not involve as much coding, but you’ll apply your
 analytical skills differently. And of course, we have two projects: - Project 1: “Crew Safety Simulator” 
using knowledge from Module 1 (damped oscillations, ODEs) to simulate the vibrations and G-forces on
 crew during a Starship launch/landing. You’ll model a simple damped mass-spring system for the crew
 cabin and see how different damping levels or trajectories impact comfort. Essentially, a tool to assess if the
 accelerations stay within safe limits (ties to SpaceX’s focus on crew safety for Starship and Dragon). - Project
 2: “Space Policy Risk Calculator” – a more open-ended project where you’ll create a framework to quantify
 the risks or compliance of a space mission with respect to regulations. For instance, input parameters of a
 mission (orbit altitude, re-entry plan, frequency use) and output a “risk score” or checklist for things like
 orbital debris, frequency interference, planetary protection, etc. You can leverage your background in
 cybersecurity/risk (GDPR/HIPAA) to draw parallels in risk scoring. The idea is to show you can engage with
 the policy side (Starlink has to coordinate spectrum and avoid collisions, etc., which is regulated).
 By completing Module 4, you’ll demonstrate that you’re not just a number-cruncher but an engineer aware
 of safety and regulatory constraints – a big plus for SpaceX, which values end-to-end mission thinking. 
Resources: - NASA Human Factor guidelines (for acceleration limits, vibration tolerances – e.g., NASA
 STD-3001 has human system integration requirements). - UNOOSA (United Nations Office for Outer Space
 Affairs) guidelines on space debris mitigation, FCC regulations for satellite constellations (for Starlink), etc.
 Even if you skim, it’s useful to know these exist. - Basic control theory for damping (optional refresh from
 Module 1 ODEs). - Any documents on SpaceX’s approach to safety (maybe NASA’s reports on Crew Dragon or
 Starship presentations that mention safety features).
 22
Weeks 1-3: Crew Safety and Damped Vibrations
 • 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
Week 1 – Human Factors & Acceleration Limits:
 Topics: Understand what humans can tolerate in terms of G-forces (launch ~4g, re-entry ~6-8g short
 spikes, ideally less), vibration (frequency and amplitude limits to avoid resonance with human body
 parts). Also, intro to how these are measured (accelerometers on crew seats, etc.).
 Readings: NASA’s Human Integration Design Handbook (if available) sections on acceleration limits.
 Also read about the Apollo or Shuttle crew G experiences for context (e.g., Apollo reentry ~6g).
 SpaceX likely aims for <4-5g for Starship crew. Find any references to Starship expected G-loads.
 Exercises: Compute the force on a 70 kg astronaut at 5g (that’s 59.8170 ≈ 3434 N). Or if a spacecraft
 vibrates at 2 Hz with amplitude 0.5g, what displacement is that? These translate abstract numbers to
 physical feel.
 ◦ 
Project 1 start: Formulate the Crew Safety Simulator:
 It will probably model the crew cabin or seat as a mass-spring-damper system. Think of the
 seat cushion as a spring-damper that buffers the crew from vibrations.
 ◦ 
◦ 
◦ 
◦ 
◦ 
Use the ODE knowledge: a second-order ODE for a damped system (m x'' + c x' + k x = F(t)).
 The input F(t) could be the acceleration profile of the rocket.
 Get a sample acceleration vs time profile for a launch or landing. You might assume one: e.g.,
 launch: ramps up to 3g over 2 minutes, then down, etc. Landing might have a quick spike.
 Start coding a simple ODE solver (you could use Python 
scipy.integrate.odeint or
 write a small RK4 integrator).
 Model: m (mass of an astronaut + seat), k (spring constant of seat cushioning/harness), c
 (damping of shock absorbers). You might need to pick values (make an educated guess or
 f
 ind something from literature: e.g., a seat might have a natural frequency ~ several Hz).
 Simulate how the acceleration of the rocket is filtered to acceleration experienced by the crew
 (the mass in the spring-damper). Essentially, you’re calculating if the seat mitigates a spike.
 SpaceX Tie-In: Connect to Starship landing: Starship flips and ignites engines just before landing 
there’s potential for high deceleration. SpaceX will need to ensure that’s within human tolerance.
 Also, vibration during ascent from 30+ Raptor engines could be intense – must be damped. Your
 simulator addresses these. Note down: “Crew safety is not just about not crashing – it’s about limiting G
forces and vibration. This simulation is like a mini version of what SpaceX does testing their seats and
 shock absorbers.”
 Week 2 – Damped Oscillations & Simulation Tuning:
 Topics: Revisit damped oscillation concepts (from Module 1 Week 4): natural frequency, damping
 ratio (under/critical/overdamped). How to interpret acceleration response.
 Readings: Briggs Ch. 16 (sections on damped systems) to refresh, or an engineering vibrations
 textbook excerpt. Also, read any info on Starship’s suspension or crew seat design if available
 (SpaceX may have mentioned cushioned landing).
 Exercises: Solve a couple of ODE problems: e.g., given m, k, c, find the damping ratio and discuss if it’s
 under or overdamped. Or find the peak acceleration transmitted for a given input using a known
 formula (shock response spectrum concept if you want to get fancy).
 Project 1 coding: Finish the core simulation:
 ◦ 
Input: an acceleration-vs-time profile (make an array for rocket acceleration).
 23
◦ 
◦ 
◦ 
◦ 
◦ 
• 
Solve the differential equation for the mass (astronaut) motion. Essentially you get x(t), and
 you can derive the acceleration of the mass relative to rocket (which is what the astronaut
 “feels” minus what the rocket does).
 Evaluate results: find peak acceleration experienced by the astronaut model and the
 maximum displacement of the spring (to check if within some limit, like seat cushion
 compression).
 Perhaps run it for a few scenarios: e.g., different damping values to see which is best (too low
 damping = oscillation, too high = too stiff).
 If possible, incorporate multiple frequency components (maybe the rocket vibration is a sum
 of a low-frequency acceleration plus a high-frequency buzz).
 Add a simple GUI or just clearly comment how to change parameters for different runs.
 Verification: If you find any data point (like “the Crew Dragon has a max of 3g during reentry because
 of flank angle” or something), see if your simulation would keep an astronaut under, say, 4g with
 chosen damping.
 • 
• 
• 
• 
• 
• 
• 
SpaceX Tie-In: In your documentation or notes, mention how Dragon or Starship likely have similar
 models. For instance, SpaceX did a lot of drop tests for Crew Dragon seats to ensure safe landing
 accelerations. Your simulator is a simplistic analog of that – a strong signal that you understand the
 human side of engineering. 
Week 3 – Wrap-Up Project 1 and Human Factors Learnings:
 Project 1 polish:
 ◦ 
◦ 
◦ 
◦ 
Ensure the simulator is user-friendly: maybe allow selecting predefined scenarios (launch vs
 landing) and output a clear summary: “Max G-force on crew = X g”.
 Possibly add a visual: plot the acceleration of rocket vs acceleration of crew mass to show
 damping effect.
 Add comments or a section in README about assumptions (e.g., “This assumes 1D vertical
 motion, ignores lateral vibrations, etc.”).
 Tie to human safety: you could add a lookup or note, like “NASA limit for sustained g is ~4g,
 our sim shows 3.5g – okay”.
 Documentation: Write the README, framing it as: “Crew Safety Simulator – Modeling how a
 damped seat system reduces launch/landing shock for Starship crew”. Explain your model and
 note what parameters one can tweak (e.g., “increase damping to see lower peak G but more
 displacement”). Mention any standards: e.g., “Per NASA guidelines, crews should experience <4 g for
 nominal missions; this tool helps estimate if a given profile meets that.”
 Project demo: If possible, record a quick demo of you running the simulation and discussing results
 (or at least include a screenshot of a plot in the repo).
 Human Factors review: Summarize key takeaways in your journal: G limits, vibration issues,
 importance of damping. Reflect on how an engineer must balance “not too stiff, not too bouncy” to
 protect crew – that systems mindset is what SpaceX needs in roles ensuring crew safety.
 Next (Policy): Prepare to shift to policy. Perhaps glance at SpaceX’s FCC filings for Starlink or any news
 (e.g., Starlink had to comply with debris rules by deorbiting sats after life, etc.). 
Weeks 4-6: Space Policy, Regulations, and Risk Analysis
 • 
Week 4 – Space Law & Policy Basics:
 24
• 
Topics: International space law treaties (Outer Space Treaty basics), national regulations (FAA for
 launches, FCC for comms, NOAA for imaging, etc.), orbital debris mitigation guidelines (e.g., deorbit
 within 25 years rule).
 • 
• 
• 
• 
• 
• 
Readings: Skim UNOOSA’s website for the main space treaties summary. Read an FAA launch
 licensing guideline summary. Also, research something specific: e.g., “SpaceX FCC Starlink license
 conditions” – see if they had to do specific debris mitigation or share spectrum info.
 Exercises: List 5 key regulations that would affect a SpaceX mission. For instance:
 Need FCC approval for Starlink frequencies.
 1. 
2. 
3. 
4. 
5. 
6. 
FAA license for each launch (including environmental assessment).
 NOAA license if doing Earth imaging.
 ITU filings for satellite orbits.
 Planetary protection if going to Mars (e.g., not contaminating Mars).
 Write a sentence how each applies.
 Project 2 planning: Design the Space Policy Risk Calculator:
 ◦ 
◦ 
◦ 
◦ 
◦ 
Define what “risks” or compliance areas to include. Possibilities: orbital debris risk (does
 mission create long-lived debris?), collision risk (for constellations), frequency interference
 risk, human safety risk (if crewed or if launch overflies population), regulatory non
compliance risk (e.g., missing a license).
 Perhaps score each on a 5-point scale and sum for a total “regulatory risk score”.
 Use your cybersecurity risk background: those fields often use matrices (likelihood vs impact).
 You could do something similar: e.g., likelihood of collision * impact (in terms of public outcry
 or damage) could be one metric.
 Plan to take an example mission (like Starlink deployment, or a hypothetical rideshare launch
 of many cubesats) and run it through your framework.
 Decide on format: maybe an interactive questionnaire (answer yes/no to certain conditions,
 then get a score), or a script where you input parameters.
 SpaceX Tie-In: Recognize that SpaceX deals with these issues: Starship launches had to get
 environmental approval (they had FAA delays due to wildlife assessments in Boca Chica). Starlink had
 to assure it won’t litter space (they have ion engines to deorbit sats). By quantifying these, you’re
 speaking the language of both engineers and policymakers – a rare combo.
 Week 5 – Build and Test Policy Risk Calculator:
 Project 2 coding: Implement the framework:
 ◦ 
◦ 
◦ 
◦ 
◦ 
◦ 
◦ 
◦ 
◦ 
You could make a simple Python script asking a series of questions, or just a function that
 takes inputs. For example:
 Input: Orbit altitude -> assign a risk: (above 600km might violate 25-year deorbit guideline
 unless propulsion).
 Input: Is satellite maneuverable? -> if no, collision risk high.
 Input: Frequency band -> if using licensed spectrum, need FCC; if not, risk if not coordinated.
 Input: Will it produce debris (like staging in orbit)? -> risk score for debris.
 Input: Reentry plan -> uncontrolled vs controlled reentry risk.
 If crewed, input: crew safety measures, etc.
 Combine scores for a total. Or output a report listing each category with a rating (low/med/
 high risk).
 Use an example to calibrate: e.g., a Starlink satellite: altitude 550km (good, under 25-year rule
 because they have propulsion, still maybe moderate risk), has propulsion (low collision risk
 25
since maneuverable), uses Ku/Ka band (spectrum allocated, low risk), etc. Should output
 mostly low risks. Another example: a hypothetical 800km altitude satellite with no propulsion-> high debris risk.
 ◦ 
• 
If you want, integrate ML: perhaps train a model on historical satellite data labeled with
 whether they became debris problems or not. But data might be scarce here. Instead, you
 might use your own rules-based approach which is fine.
 Testing: Run a few scenarios:
 ◦ 
◦ 
◦ 
◦ 
◦ 
• 
Scenario A: Falcon 9 launch of 60 Starlinks – should be mostly compliant (SpaceX planned
 carefully).
 Scenario B: A rideshare dumping 50 small sats at 600km, many with no propulsion – highlight
 higher risk in output.
 Scenario C: Starship going to Mars – see if planetary protection should be a factor (it would,
 but SpaceX likely to ignore if not NASA-funded; still, Outer Space Treaty stuff).
 Scenario D: A reentry of Starship over land – violation of safety best practices maybe.
 These are hypothetical, but it shows your tool’s flexibility.
 Documentation: Write up the logic and references if any. E.g., “Based on the U.N. debris mitigation
 guidelines (25-year rule), missions above LEO without deorbit plan get a high score in debris risk.” If
 possible, cite a line from a source about debris guidelines.
 • 
• 
• 
• 
• 
• 
• 
• 
• 
User Interface: If time, make it a bit interactive or at least clearly explain how to input values. Possibly
 create a JSON or YAML config for a mission that the script reads, to simulate a real “analysis tool”.
 SpaceX Tie-In: Emphasize that you included SpaceX-relevant factors: e.g., for Starlink the biggest
 regulatory risk was spectrum and debris; for Starship, environmental and planetary protection.
 Mention that you used your compliance background to approach space missions systematically 
something not many aerospace folks have, giving you a unique edge.
 Week 6 – Module 4 Synthesis and Portfolio:
 Complete Project 2: Finalize any tweaks, ensure it’s on GitHub with a descriptive README (“Space
 Mission Regulatory Risk Analyzer” might be another name).
 Demonstration: Since this project is more conceptual, a video demo might just be you walking
 through the code logic or a sample output. Or create a sample “report” output and show it.
 Review: Summarize key points of space policy you learned. You don’t need to memorize laws, but you
 should be aware of the context—SpaceX operates under constraints (cannot just launch whenever/
 wherever without approval). This awareness can impress in interviews if you mention, for example, 
“I’m mindful of the FCC requirements on mega-constellations – in fact, I built a tool to assess such
 compliance.”
 Networking: By now, you could reach out to perhaps a SpaceX regulatory or mission assurance
 employee (they exist on LinkedIn) and express interest in that side of things, mentioning your
 project. It’s a more niche area, but connections here could set you apart.
 Portfolio update: Add these Module 4 projects to your portfolio page/LinkedIn. Highlight the breadth:
 you now have technical sims AND policy tools.
 Transition: Get ready for Module 5, which will swing back to a mix of advanced technical
 (astrophysics) and heavy ML – essentially your wheelhouse combining space and ML.
 Take a breather – Module 4 was different but vital. You’ve rounded out your knowledge to include what
 many self-study engineers ignore. This holistic perspective is something SpaceX values (they need
 engineers who grasp the whole mission, not just isolated calculations). 
26
Module 5: Astrophysics and Advanced Machine Learning (8 Weeks)– Space Data and Autonomy
 Module Overview: Module 5 leverages your machine learning background in the context of space and
 astrophysics. As SpaceX pushes toward autonomous operations (think Starship’s autonomous landing,
 Starlink satellites avoiding collisions), ML and data science are increasingly important. Also, understanding
 the space environment (radiation, solar activity) is crucial for designing resilient systems. In this module,
 you’ll blend astrophysics topics (orbital perturbations, space weather) with ML techniques. Two projects: 
Project 1: “Orbital Anomaly Detector” – Using historical orbital data (or simulated anomalies) to train a
 model (possibly a neural network with PyTorch) that can detect anomalies in satellite orbits. For example, if
 a satellite’s orbit changes unexpectedly (could indicate collision or system failure), the model flags it. This
 parallels how you did fraud detection, but for spacecraft – demonstrating transfer of your ML skills to
 aerospace. - Project 2: “Solar Flare Predictor” – Training an ML model on solar weather datasets to predict
 solar flares or high radiation events. SpaceX (with Starlink) cares about this because solar flares can disrupt
 communications and even cause atmospheric expansion (drag) that deorbits satellites (as happened in 2022
 when a solar storm caused premature reentry of some Starlinks). This project showcases applying ML to
 astrophysics data, a strong signal of interdisciplinary skill.
 By the end of Module 5, you’ll have solid examples of using ML in aerospace contexts, aligning with SpaceX’s
 trend of using AI (they even have roles for ML in rocket design, Starlink network optimization, etc.). You’ll
 also deepen your knowledge of space environment and orbital dynamics complexities beyond two-body
 mechanics (like perturbations, atmospheric effects – some of which you touched earlier).
 Resources: - SpaceTrack or Celestrak data on satellite orbits (two-line elements over time) – maybe use
 these for anomaly detection. - NASA OMNI dataset or other space weather databases (for solar flares,
 geomagnetic indices, etc.). - Courses: Coursera’s “Machine Learning for Earth and Space Sciences (Caltech)”– perfect fit here. If enrolled, apply its content to these projects. - PyTorch or TensorFlow documentation (to
 refresh building a model). - Research papers or articles on using ML for satellite anomaly detection or space
 weather prediction (if any, to get ideas).
 Weeks 1-4: Orbital Data Analysis & Anomaly Detection
 • 
• 
• 
• 
• 
Week 1 – Orbital Perturbations & Data Gathering:
 Topics: Beyond J2: other perturbations like solar radiation pressure, third-body (sun/moon) effects,
 and operational anomalies (satellite maneuvers or malfunctions). How these appear in orbital data.
 Readings: Look up articles on notable satellite anomalies (e.g., a satellite suddenly lowered orbit due
 to drag from a geomagnetic storm, or one that exploded creating debris). Celestrak might have
 some analysis posts. Also, read about how NORAD tracks orbits via TLEs.
 Data collection: Download some orbital data for a satellite over time. Space-Track.org provides TLE
 history if you have an account (maybe use a publicly available set from Celestrak – some have epoch
 times listed). Alternatively, simulate anomalies: you could propagate an orbit and then simulate a
 small change (like a drag event).
 Exercises: Basic analysis: given two TLEs at different times, compute the difference in mean motion or
 semi-major axis – infer if orbit is decaying. Do a rough calculation: if a Starlink drops altitude by 20
 km overnight, what could cause that? (Perhaps a solar storm increased drag).
 27
• 
Project 1 setup: Plan the anomaly detector:
 ◦ 
◦ 
◦ 
◦ 
◦ 
• 
Decide what features to use. Perhaps you’ll use time-series of orbital elements (like semi
major axis, eccentricity, inclination over time).
 An anomaly could be defined as a sudden change beyond normal thresholds (this could be
 unsupervised anomaly detection or supervised if you label events).
 If using ML, you might create a training set of “nominal” vs “anomalous” sequences. Possibly
 simulate anomalies (like a big drop in alt or jump in inclination).
 Tools: use PyTorch (since you’re comfortable) to perhaps create an LSTM or another
 sequential model that learns the normal pattern and flags deviations.
 Alternatively, use simpler ML first: maybe a Random Forest on differences, or even a
 statistical control chart approach.
 SpaceX Tie-In: Starlink operations: SpaceX needs to know if one sat is off-nominal (e.g., lost
 propulsion and is falling). They likely have automated systems for this. You building one shows
 initiative. Also, any collision avoidance (Starlink dodging other objects) – anomaly detection helps
 f
 lag risk events.
 • 
• 
• 
• 
• 
• 
• 
• 
Week 2 – ML Model Development (Orbital Anomaly):
 Project 1 coding: Start building the dataset and model:
 ◦ 
◦ 
◦ 
◦ 
◦ 
◦ 
Preprocess orbit data: for example, create a time series of altitude for a satellite. Smooth it or
 compute first differences.
 Label or mark anomalies: e.g., inject a synthetic event like a sudden 5% drop in semi-major
 axis at a certain time.
 Choose a model: maybe an LSTM autoencoder that learns to reconstruct normal sequences
 and fails on anomalies, or a simple approach like thresholding velocity of change.
 Implement the model using PyTorch. If new to PyTorch, use this time to practice a small RNN
 on dummy data first.
 Train on “nominal” data (could be a portion of the sequence without events).
 Test on data with an event to see if it flags it (like an anomaly score spikes).
 Readings/Videos: Use Coursera or other ML-for-physics resources to guide model selection. There
 might be an example of anomaly detection (sometimes taught in sequence modeling context).
 Exercises: Refresh ML basics: for example, manually work through a simple time series anomaly by
 calculating a moving average and seeing when something deviates by >3σ (statistical anomaly
 detection). This could complement the ML approach.
 Validation: If possible, find a real anomaly case: e.g., search if “Kosmos-**** satellite breakup TLE
 changes” – maybe data available to test your detector. If not, rely on simulated anomalies.
 Iteration: Tweak model as needed (maybe the first approach flags too many false positives; adjust
 threshold or model complexity).
 SpaceX Tie-In: Document an example: “In a constellation like Starlink, if one satellite experiences
 increased drag from a solar storm, its orbit will decay faster. My model should catch that by noticing the
 semi-major axis dropping abnormally compared to others.” This shows you understand both the
 physics (drag, solar storm) and the solution (ML monitoring).
 Week 3 – Finalize Anomaly Detector & Results:
 28
• 
Project 1 finishing:
 ◦ 
◦ 
◦ 
◦ 
• 
Evaluate the model performance: false alarms vs missed detections. For fun, compute
 something like precision/recall if you have multiple injected anomalies.
 Create visualization: plot orbital parameter over time with anomaly regions highlighted, to
 include in your repo or discussion.
 Write up usage instructions: e.g., how to feed new data into the model to check for
 anomalies.
 Consider extending to multiple satellites: e.g., a multivariate approach where you compare
 one satellite’s behavior to the fleet (an outlier detection across the constellation).
 Documentation: In README, describe the problem and solution: “This tool uses an LSTM neural
 network to learn normal orbital behavior of satellites and detect anomalies such as sudden
 orbit changes or unexpected maneuvers.” Mention data sources (even if simulated) and the
 motivation (collision avoidance, satellite failures).
 • 
• 
• 
• 
• 
• 
• 
• 
Project integration: If you did the Coursera ML for Earth/Space, mention that you applied concepts
 from it here – adds credibility. Maybe even cite a paper if you found one (though not required).
 Module 5 Midpoint Review: You’ve done heavy ML; check that you still remember the space context 
e.g., could you explain to someone why a solar storm can cause orbital decay? If not, revisit a source
 on that. It’s important to link the ML output to physical reasoning when talking about it.
 Week 4 – Space Weather 101 (Solar Physics):
 Topics: Basics of the Sun’s influence: solar flares, coronal mass ejections (CMEs), geomagnetic storms,
 radiation belts. How they affect spacecraft (radiation damage, drag increase from heated
 atmosphere, comms blackout).
 Readings: NASA or NOAA resources on space weather (NOAA’s Space Weather Prediction Center has
 info). Look at historical events like the Carrington Event (huge solar storm) or more recent ones (e.g.,
 the Feb 2022 storm that caused 40 Starlinks to fail right after launch ).
 Exercises: Look up a dataset of solar flux (e.g., F10.7 index) and see if you can correlate it with
 atmospheric drag. Simple exercise: find if a spike in solar flux corresponds to higher drag (which
 might be tough for you to measure, but conceptually).
 4
 Project 2 planning: Outline the Solar Flare Predictor:
 ◦ 
◦ 
◦ 
◦ 
◦ 
◦ 
Get data: perhaps NOAA provides past solar flare events and associated indicators (like X-ray
 f
 lux). The GOES satellite data might have the X-ray flux time series and flare listings (M-class,
 X-class flares etc.).
 Choose an ML approach: this could be a time series classification (predict if a flare will occur
 in next 24h from current data) or regression (predict solar flux level).
 A common approach is to use historical sunspot numbers or X-ray flux as input to predict
 f
 lares (some research does this with e.g. LSTM or even computer vision on solar images – but
 we likely stick to time series).
 You could simplify by trying to classify days as “flare” or “no flare” based on previous days’
 data.
 Tools: likely use PyTorch or sklearn again.
 Alternative: If data is limited, perhaps focus on predicting radiation index (Kp or ap index)
 from solar measurements.
 SpaceX Tie-In: Why do we care? SpaceX has to sometimes delay launches due to solar storms, Starlink
 satellites use info to plan to dodge bad events, and for crewed missions radiation is a big concern.
 Write down: “SpaceX mission planners monitor solar weather to protect satellites and crew. An ML model
 29
that can forecast flares or high radiation could inform decisions like delaying a launch or safe-mode for
 satellites.”
 Weeks 5-8: Solar Flare Prediction ML Project
 • 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
Week 5 – Data Prep and Exploratory Analysis (Solar ML):
 Data acquisition: Download relevant datasets:
 ◦ 
◦ 
◦ 
NOAA’s GOES X-ray flux data (they have 5-minute values, and lists of flares).
 Perhaps sunspot numbers or solar flux index (F10.7 cm flux).
 Maybe create a labeled dataset: e.g., for each day (or each rotation of sun ~27 days), mark
 whether an X-class flare occurred.
 Exploratory analysis: Plot the solar X-ray flux over a period with a known flare to see the pattern.
 Check correlations: e.g., do high sunspot counts correlate with flares (they should, generally more
 sunspots => more flares).
 Exercises: Calculate some stats: average number of flares per solar cycle phase, etc. This helps
 understand the data distribution.
 ML approach: Decide: classification (flare vs no flare) might be easiest. Possibly use a sliding window
 of time series (past N hours of flux readings) to predict if a flare (above certain threshold) will happen
 in next hour.
 Model building: Start with a simple model to test feasibility – e.g., logistic regression or random forest
 on features like recent flux average, trend, etc. See if there’s any predictive signal.
 If not promising: It’s known that flare prediction is a hard research problem. But even a modest
 accuracy is something. You could also pivot slightly: maybe predict the impact of flares (like predict
 Kp index, which is easier as it correlates with solar wind).
 Keep scope reasonable: If direct prediction is too hard, consider instead building a model that alerts
 when conditions are ripe for flares (like high sunspot count, active regions visible). This could be
 simpler classification.
 4
 SpaceX Tie-In: Think of framing – even if the model isn’t super accurate, the exercise shows you
 applying ML to space data. SpaceX Starlink engineers had a real case of flare causing satellite loss
 . If you mention that event and how a predictor could help avoid such losses by not launching
 during a high-risk window, that’s impactful.
 Week 6 – ML Model Development (Solar Predictor):
 Coding: Implement the chosen model (if sticking with PyTorch, maybe an RNN on time series; or use
 scikit-learn if simpler).
 Training: Train on historical data (e.g., use a few years of data to predict flares).
 Evaluation: Measure performance – true/false positives. Don’t worry if it’s not great (even
 professional models have maybe ~70% accuracy for big flares).
 Improve: Try adding features (maybe incorporate multiple sources: X-ray plus magnetic indices).
 Results: Save model outputs like a graph of predicted vs actual flares.
 Real-time simulation: You could test on recent data in a sliding way, to mimic how it’d perform in
 operation.
 User perspective: Perhaps design it so the input can be current solar data and it prints a probability of
 f
 lare. That’s a tangible output someone at SpaceX might want (like an alert percentage).
 Documentation: Start writing up the methodology and citing sources of data.
 30
• 
Exercises: Refresh any astrophysics behind solar flares – be ready to explain in simple terms what
 causes a flare and why it’s unpredictable, to contextualize the difficulty.
 • 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
Week 7 – Finalize Solar Predictor and Documentation:
 Finalize Project 2:
 ◦ 
◦ 
◦ 
Ensure code is clean and parameters can be adjusted (like prediction window).
 Write the README describing the data, model, and how to interpret output.
 Include any charts or examples. For instance: “On [date], model predicted high flare probability
 and indeed an M-class flare occurred 6 hours later.” If you find such a case, great anecdote.
 Potential expansion: If time, consider merging Projects 1 & 2 insights: a comprehensive “space risk
 predictor” – e.g., feed a predicted solar event into your anomaly detector to see if it would catch the
 resulting orbit changes. This might be too much, but conceptually linking them is nice to mention.
 Portfolio integration: Now your portfolio has 10 projects! Possibly condense for presentation. You
 might merge some or highlight key ones. But having them separate is fine; just plan how to
 communicate them succinctly.
 ◦ 
◦ 
Week 7 Review: Step back and list what advanced skills you demonstrated:
 ML (PyTorch models, anomaly detection, time-series forecasting).
 Working with real scientific data (TLEs, solar data).
 ◦ 
◦ 
Domain knowledge in astrodynamics and space environment.
 This is resume gold – think how to phrase it. For example, “Developed LSTM-based anomaly
 detection for satellite orbits” and “Built machine learning model to forecast solar flare activity
 impacting satellite operations.”
 Networking: This is a good time to perhaps write a blog post on Medium or LinkedIn about one of
 these ML projects. Content like “Using AI to Protect Satellites from Space Weather” could attract
 attention and shows thought leadership. If comfortable, do it.
 Week 8 – Module 5 Wrap-Up & Capstone Prep:
 Review & Quiz: Ensure you can explain key astrophysics concepts (like what’s a solar flare, what’s drag,
 etc.) clearly. Quiz yourself or have a friend ask you.
 Certifications: If you took the Coursera ML for Earth/Space, finalize it and get the certificate. This is
 directly relevant – add to resume.
 Prep for Capstone: The capstone will integrate everything – start thinking of an outline for it. It’s
 essentially “Starship Mars Mission Simulator” which means combining orbital (Module2), vehicle
 performance (Module3), maybe human factors (Module4), and using ML (Module5) for optimization/
 anomaly detection. In the next module, you’ll bring pieces together. Perhaps list which of your
 existing code can be reused or needs adaptation for capstone.
 Portfolio & Resume: Update everything with Module 5 achievements. You’re nearly done – one more
 big push!
 31
Module 6: Electives and Capstone Integration (6+ Weeks) – 
Specializations and Final Synthesis
 Module Overview: The final module is two-fold: a short Electives section to cover any remaining topics of
 interest or gaps (e.g., deep dive into rocket engines and cybersecurity as mentioned), and then a Capstone
 Project (4-6 weeks) that brings it all together into a comprehensive Starship Mars Mission Simulator. This
 capstone is your crowning achievement to show SpaceX. It will simulate a full mission profile: launch, orbit,
 trans-Mars injection, cruise, landing – incorporating physics, controls, maybe some ML for anomaly
 handling, and human factors. Essentially a mini-version of what SpaceX would do in a Mars mission
 feasibility study, packaged into a single GitHub repo and video.
 Elective Projects (Module 6 Part 1): - Project 1: “Raptor Engine Propulsion Model” – a deep dive into
 rocket engine performance. You’ll simulate thrust curves of a multi-engine setup (e.g., Starship’s 33 Raptor
 engines) and see how throttling or engine-out affects performance. Possibly optimize for minimal fuel
 usage for a given trajectory (ties to Module3 trade study but on a finer level). This leverages Sutton’s rocket
 engine knowledge and gives you cred in propulsion. - Project 2: “Satellite Cybersecurity Simulator” 
combining your IT/cyber skills with space. Model a scenario of a cyber-attack on a satellite network (like
 jamming or hacking a comm link) and use your security background to propose mitigations. This is more
 conceptual/simulation (maybe write a script that “encrypts” a data stream and show how it prevents an
 interception). It’s a chance to highlight your prior experience in a space context (Starlink network security
 concerns).
 After electives, the Capstone (Final Project) will be: - “Starship Mars Mission Simulator” – An end-to-end
 simulation of a mission: - Launch: Use your ascent sim (Module1/2) to get to orbit. - Orbit: Compute a
 Hohmann transfer to Mars (Module2). - In transit: maybe simulate a course correction or an anomaly
 (Module5 input, like a solar flare event requiring correction). - Mars entry/landing: simulate a powered
 descent (could reuse your damping model or just approximate deceleration). - Include subsystem checks
 (Module3 trade outputs, like ensure enough fuel). - Incorporate human factors: check G-forces on crew at
 launch and landing (Module4). - Use ML if possible: perhaps to optimize the trajectory for minimum fuel or
 predict risks. - Validate parts with GMAT or known data. - Present it as a coherent software tool or report.
 This is ambitious, but remember, you can reuse lots of what you’ve built, linking them in a storyline rather
 than coding everything from scratch.
 Outcome: By finishing the capstone, you’ll have demonstrated capability across the board, essentially doing
 a mini space mission design all by yourself. Sharing this (code + a slick video with narration as if you’re
 mission control) will be extremely impressive to SpaceX or any aerospace employer.
 Electives (Week 1-2): Raptor Propulsion Deep-Dive
 • 
• 
• 
Week 1 – Rocket Engines and Thrust Simulation:
 Topics: Thrust equation details ($F = \dot m * v_e + (P_e - P_{amb})A_e$), engine throttling, gimbal,
 and multi-engine effects (engine-out scenarios). Raptor specific: methane fuel, staged combustion.
 Readings: Sutton’s Rocket Propulsion Elements (chapter on engine performance, nozzle expansion).
 SpaceX materials on Raptor (there are Elon’s tweets or presentations outlining ISP, thrust). Also,
 maybe research how engine-out is handled (Falcon 9 can lose an engine and still make orbit).
 32
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
Exercises: Calculate thrust for a given mass flow and exhaust velocity. E.g., if Raptor has Isp ~350 s at
 sea level, what mass flow gives 2 MN thrust? Also compute effect of altitude on thrust (as ambient
 pressure drops, thrust rises for fixed chamber pressure).
 Project work: Develop Raptor Propulsion Model:
 ◦ 
◦ 
◦ 
◦ 
◦ 
Write a function to compute thrust over time given throttle setting. Use Raptor published
 data: e.g., 100% throttle ~230 ton-force at sea level.
 Model multiple engines: sum thrust, maybe random failure of one engine at a certain time
 and show how total thrust dips.
 Simulate a simple ascent: combine with your rocket sim but focusing on the thrust curve. E.g.,
 throttle down at Max Q, throttle up, then engine cutoff.
 Perhaps incorporate fuel consumption: track mass reduction over time from $\dot m$.
 Optimize: perhaps run a simple loop to see what throttle profile minimizes max G or
 maximizes efficiency.
 SpaceX Tie-In: Express understanding of Starship’s propulsion: “Starship’s 33 Raptors provide massive
 thrust (~75 MN total). This model shows how losing one engine (engine-out) only drops thrust by ~3%,
 which is why Starship can tolerate failures.” If you simulate engine-out and see minor trajectory
 change, that’s a great point.
 Week 2 – Satellite Communications & Cybersecurity:
 Topics: Basics of satellite communications (frequencies, encryption), threats to satellites (jamming,
 spoofing, cyberattacks on ground systems). Starlink’s network security considerations.
 Readings: Possibly a whitepaper or article on satellite cybersecurity (there have been conferences on
 this). Also, recall your knowledge of GDPR/HIPAA – not directly applicable, but risk assessment
 methodologies are.
 Exercises: Enumerate threat scenarios for Starlink: e.g., hacker tries to take control of a ground
 station, or adversary jams the uplink. Consider impacts.
 Project work: Outline Satellite Cyber Simulator:
 ◦ 
◦ 
◦ 
◦ 
It might be more of a conceptual simulator: e.g., model nodes (satellites, user terminals,
 ground stations) in a network graph. Simulate a “attack” by removing or compromising a
 node, and see effect (like loss of coverage or data).
 Or create a simple script showing data encryption: take a message, “send” it with encryption
 vs without to demonstrate interception ease vs difficulty.
 If you have networking experience, maybe simulate a denial-of-service on a satellite link (just
 conceptually, like measuring bandwidth drop).
 The result should be insights like: “If one gateway is hacked, Starlink has many others, so
 redundancy helps. But if encryption is weak, intercepting traffic could reveal user data.”
 Deliverable: Perhaps produce a short report rather than heavy code. It could be a markdown in the
 repo: listing threats and mitigations. If code, maybe a small Python illustrating one aspect (like a
 Monte Carlo simulation of network resilience).
 SpaceX Tie-In: SpaceX certainly cares about this: Starlink is critical infrastructure, and Elon has spoken
 about security (there were reports of researchers hacking a Starlink dish). By addressing this, you
 show forward-thinking beyond traditional aerospace. Mention: “Using my IT security background, I
 assessed Starlink’s network risks, which is something many aerospace engineers overlook.”
 With electives done, ensure you document these projects (they might be smaller than previous ones, which
 is okay). Now, onto the grand finale.
 33
Capstone (Weeks 3-6): Starship Mars Mission Simulator
 • 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
Week 3 – Capstone Planning and Architecture:
 Define scope clearly: You have many pieces; decide the mission flow and which parts to implement vs
 describe:
 1. 
2. 
3. 
4. 
5. 
6. 
7. 
Launch & Ascent: Use your Rocket Ascent Simulator to simulate launching Starship (with
 Super Heavy booster) to orbit. You might not have staged in original sim, so possibly simplify:
 assume booster gets it to near orbital velocity, then Starship handles final insertion.
 Orbital Refueling (optional): Mention it but you could skip simulating actual refuel (or just
 say Starship refuels in LEO).
 TLI (Trans-Lunar Injection) or TMI (Trans-Mars Injection): Use your Module2 transfer calc
 to send Starship toward Mars. Compute delta-V required and ensure it’s <= Starship capability
 (tie to Module3 trade calc to see if payload fits).
 Cruise & Anomalies: During transit, maybe incorporate a solar flare event – use your
 predictor to say one is coming, and adjust spacecraft (maybe put it in a safe mode, which you
 can simulate by altering trajectory slightly or just noting).
 Mars Arrival: Simulate a braking burn or aerocapture. Could use a simple adaptation of your
 projectile sim for Mars gravity (and thin atmosphere drag if daring).
 Landing: Use a vertical landing sim – similar to your damped landing model, see what G’s
 might be on crew on final burn.
 Post-landing: Success criteria (did you land within delta-V budget, were G-forces safe, etc.).
 Integration: Decide how to integrate code. Possibly create a single Jupyter Notebook or script that
 calls functions from your previous projects in sequence. You might need to modify some to work
 together (e.g., output of ascent sim becomes input to transfer calc).
 ◦ 
Validation: Plan to check some parts with GMAT or known data:
 Orbits: ensure your Earth-Mars transfer time matches ~6-8 months.
 ◦ 
Fuel: use rocket equation to see if Starship could carry enough prop (Starship likely needs
 refuel – incorporate that).
 Visualization: A mission plot would be great (e.g., orbits of Earth and Mars and the transfer
 trajectory). Perhaps use poliastro or matplotlib to draw orbits.
 Work division: This is heavy – allocate tasks to each remaining week.
 SpaceX Tie-In: This is essentially a SpaceX mission plan. Frame it as such: you’re demonstrating an
 understanding of what SpaceX ultimately is trying to do – go to Mars. Musk has said the whole point
 of SpaceX is enabling multiplanetary life. By simulating a Mars mission, you speak directly to that
 vision.
 Week 4 – Build Capstone Part 1 (Launch to TMI):
 Launch Simulation: Adapt your ascent sim for two-stage: you might simulate booster and ship
 separately (maybe do a two-phase sim: booster burnout at e.g. 1700 m/s, then second stage to 7800
 m/s). Or simplify by injecting directly to orbit with required delta-V.
 Ensure you capture key outputs: max Q or max G perhaps, final orbital parameters.
 Orbit & Transfer: Use Module2 code to calculate the window and delta-V for Mars transfer.
 Incorporate the date or phase angle for departure. Determine if you need a plane change or assume
 co-planar (for simplicity, assume perfect alignment and launch window).
 Deduct the propellant for TMI burn from Starship’s fuel (which came with full tanks due to refueling).
 34
• 
Check budgets: Use Module3 trade sim to see if Starship’s mass and delta-V are enough for this TMI
 after reaching orbit. (Starship in orbit fully fueled ~1200t gross, needs ~(?) m/s to Mars – presumably
 f
 ine with refuel).
 • 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
Coding: Write this as a cohesive script up to leaving Earth:
 ◦ 
Maybe structured as: 
simulate_launch() -> results , then 
compute_transfer() ->
 results.
 Documentation as you go: Comment and note assumptions (like “assuming instant transfer burn at
 LEO, ignoring inclination differences” etc.).
 Intermediate Verification: If you have GMAT, you could set up an Earth-Mars transfer for the same
 epoch and see if arrival date matches. Or use poliastro’s porkchop plotting to ensure you picked a
 reasonable launch window. But don’t get too bogged – a basic consistent story is enough.
 Week 5 – Build Capstone Part 2 (Cruise to Landing):
 Cruise & Anomaly: Decide on an event: maybe halfway to Mars, a solar storm hits. Show that your
 Solar Flare Predictor would have given a warning (if you have actual date data, find one around a
 recent mission).
 Perhaps simulate a small course correction burn (couple m/s) that might be needed due to that or to
 f
 ine-tune trajectory.
 Mars Arrival: Simulate approach. Possibly do a reverse of TMI – a Mars orbit insertion burn or direct
 landing.
 If doing direct entry: simulate aerodynamic braking – you might use a simple model (like treat
 Starship as having a certain ballistic coefficient, compute deceleration).
 Then a final retropropulsive burn to land. Use your damping model to estimate G-forces on landing
 (Mars gravity is 0.38g, so maybe a bit easier).
 Landing zone: maybe assume they aim for a specific site. It’s extra, but mentioning precise landing
 targeting shows detail-orientation.
 Coding: Continue the script:
 ◦ 
◦ 
After transfer, do 
simulate_entry_and_landing() . This could reuse the projectile code
 with Mars parameters (lower gravity, some thin drag).
 Or if short on time, simply calculate needed delta-V to land and assume a profile (like 4g
 deceleration).
 Results: Key outputs:
 ◦ 
◦ 
◦ 
◦ 
◦ 
Total mission delta-V used vs available (did we have margin?).
 Max G on launch and landing.
 Time of flight to Mars.
 If any anomalies (maybe simulate one engine out during landing and see if still okay).
 Anything interesting like fuel remaining.
 Wrap it up: Conclude with success (or identify if it fails in simulation).
 Validation: Compare your numbers to known: e.g., typically Earth-Mars ~6-7 months, Isp/delta-V
 needed ~??. If something is way off, adjust assumptions.
 Week 6 – Capstone Finalization and Presentation:
 Testing: Run the full simulation end-to-end. Fix any bugs or unrealistic results by tweaking.
 35
• 
• 
• 
• 
• 
• 
◦ 
Documentation: This project needs a solid README or even a short PDF report:
 Introduction: mission overview.
 ◦ 
◦ 
◦ 
Methods: what you simulated (with references to modules/code).
 Results: key findings, maybe a table of phases with delta-V, time, G-forces.
 SpaceX relevance: highlight how this sim could be used to evaluate mission feasibility or to
 demonstrate you understand the mission profile.
 Video Presentation: This is crucial for “GitHub visibility.” Create a compelling 3-5 minute video that
 walks through the mission:
 ◦ 
◦ 
◦ 
Perhaps use slides or an animation of the trajectory (if you can generate using matplotlib or
 even manually draw).
 Talk as if you’re presenting a mission plan: “Launch: nominal, Max G 3.8, orbit achieved. Trans
Mars burn of 3.6 km/s performed – on course to Mars. During coast, a solar flare was
 detected by onboard AI (our anomaly detector) – Starship switched to safe mode for 12
 hours. Approaching Mars, performed entry burn... etc. Finally landed with 200 m/s of fuel
 remaining – within safety margins. Crew experienced peak 5g decel on landing, which is high
 but tolerable for short duration with couches.”
 This narrative style, backed by your simulation data, will impress. It shows technical skill and
 the ability to communicate a mission.
 Submit and Share: Upload the video (unlisted YouTube or Google Drive). Provide link in your GitHub
 or resume. This is something you can send to a SpaceX recruiter or discuss in an interview.
 Resume Polishing: Now update your resume to prominently feature the capstone and a skills
 summary. E.g., “Capstone – Starship to Mars Simulation: Developed end-to-end Python simulation
 of a crewed Mars mission, including launch dynamics, orbital mechanics, ML-based anomaly
 detection, and landing analysis. Demonstrated integration of multidisciplinary aerospace
 engineering concepts.”
 Apply to SpaceX: With all this done, you are in a great position. Use the networking you've done, the
 AIAA membership (maybe you’ve gotten some contacts or asked for resume review), and start
 applying to relevant roles. Tailor your cover letter to talk about these projects – far more compelling
 than just a degree.
 Continued Learning: Even though the structured program is done, space is vast. Keep following
 SpaceX news, join online forums (like the SpaceX subreddit or NASA Spaceflight forums) to stay
 updated. And maybe start a new project or contribute to open-source space software to keep sharp.
 Conclusion: You now have an Ultimate Self-Study Portfolio tailored for SpaceX success: - 12 projects on
 GitHub (+capstone), each tying directly to SpaceX needs (from orbital simulators to ML tools). - Knowledge
 covering math, physics, coding, space systems, human factors, and policy – truly end-to-end. - Certifications
 and networking connections to bolster your profile. - The confidence of having essentially done a mock
 SpaceX project solo.
 SpaceX hires those who show they can solve hard problems and have a passion for the mission .
 Through this program, you’ve proven both. Keep that passion burning (figuratively, not literally like a Raptor
 engine) and good luck – you’re much closer to that SpaceX dream than 56 days ago, and the sky (or rather,
 Mars) is no longer the limit. Ad Astra! 
1
 36
1
 4
 It Took Elon Musk Exactly 5 Words to Reveal What He Looks for in Every New Hire (and It's Not a
 College Degree)
 https://www.inc.com/justin-bariso/it-took-elon-musk-exactly-5-words-to-reveal-what-he-looks-for-in-every-new-hire-and-its-not-a
college-degree.html
 2
 Software Engineer, Flight Software (Starship) at SpaceX
 https://startup.jobs/software-engineer-flight-software-starship-spacex-6713242
 3
 General Mission Analysis Tool (GMAT)
 https://etd.gsfc.nasa.gov/capabilities/capabilities-listing/general-mission-analysis-tool-gmat/
 37