WavDataExtractor extractor;
FlowField baseFlowField;
FlowField specialFlowField;
Particle[] baseParticles;
Particle[] specialParticles;
int storyCounter = 0;
int totalStories = 0;
int noOfPoints = 4000; // Number of particles
color col;

void setup() {
  size(800, 600, P2D);
  showSetup();
  countWavFiles();
}

void showSetup(){
  background(0);
  hint(DISABLE_DEPTH_MASK);
  baseFlowField = new FlowField(40); // Grid scale for the base FlowField
  specialFlowField = new FlowField(40); // Grid scale for the special FlowField
  baseParticles = new Particle[noOfPoints];
  specialParticles = new Particle[noOfPoints];
  col = color(random(55), random(255), random(100));
  for (int i = 0; i < noOfPoints; i++) {
    baseParticles[i] = new Particle(color(255, 0, 0)); // Red particles for base show
    specialParticles[i] = new Particle(col); // Random color for special show
  }
}

void baseShow(){
  fill(0, 6); // Trail length
  rect(0, 0, width, height);
  baseFlowField.update();
  for (int i = 0; i < baseParticles.length; i++) {
    PVector force = baseFlowField.lookup(baseParticles[i].pos);
    baseParticles[i].follow(force);
    baseParticles[i].update();
    baseParticles[i].edges();
    baseParticles[i].show();
  }
}

void specialShow(){
  col = getColorBasedOnStoryCounter(storyCounter); // Update color based on storyCounter
  fill(0, 6); // Trail length
  rect(0, 0, width, height);
  specialFlowField.update();
  for (int i = 0; i < specialParticles.length; i++) {
    specialParticles[i].setColor(col); // Update color of each particle
    PVector force = specialFlowField.lookup(specialParticles[i].pos);
    specialParticles[i].follow(force);
    specialParticles[i].update();
    specialParticles[i].edges();
    specialParticles[i].show();
  }
}

int getColorBasedOnStoryCounter(int counter) {
  // Dictionary of colors
  HashMap<Integer, Integer> colorDict = new HashMap<Integer, Integer>() {{
    put(1, color(255, 0, 0));     // Red
    put(2, color(0, 255, 0));     // Green
    put(3, color(0, 0, 255));     // Blue
    put(4, color(255, 255, 0));   // Yellow
    put(5, color(255, 165, 0));   // Orange
    put(6, color(128, 0, 128));   // Purple
    put(7, color(255, 192, 203)); // Pink
    put(8, color(165, 42, 42));   // Brown
    put(9, color(128, 128, 128)); // Gray
    put(10, color(0, 0, 0));      // Black
  }};
  return colorDict.getOrDefault((counter % 10) + 1, color(255, 255, 255)); // Default to white if not found
}

void showManager(){
  if (extractor == null || !extractor.player.isPlaying()) {
    baseShow();
  } else {
    specialShow();
  }
}

void draw() {
  showManager();
  countWavFiles();
  if (totalStories > 0) {
    println("totalStories > 0: " + totalStories);
    if (extractor == null) {
      println("extractor is null, playing next story");
      playNextStory();
    } else {
      extractor.update();
      if (!extractor.player.isPlaying()) {
        playNextStory();
      }
    }
  } else {
    println("Waiting for story part: " + storyCounter);
  }
}

void stop() {
  if (extractor != null) {
    extractor.close();
  }
  super.stop();
}

void countWavFiles() {
  File folder = new File(sketchPath("data"));
  File[] listOfFiles = folder.listFiles();
  int count = 0;

  if (listOfFiles != null) { // Ensure listOfFiles is not null
    for (File file : listOfFiles) {
      if (file.isFile() && file.getName().endsWith(".wav")) {
        count++;
      }

      if (storyCounter > 0 && file.getName().equals("story0.wav")) {
        println("Found story0.wav");
        storyCounter = 0;
      }
    }
  }

  totalStories = count;
  println("Counted files: " + totalStories);
}

void playNextStory() {
  if (extractor != null) {
    extractor.close();
  }
  String filePath = String.format("data/story%d.wav", storyCounter);
  extractor = new WavDataExtractor(this, filePath);

  // Call showManager before playing the next story
  showManager();

  extractor.player.play();
  storyCounter++;

  // Delete the file after playing
  File playedFile = new File(sketchPath(filePath));
  if (playedFile.exists()) {
    playedFile.delete();
  }
}
