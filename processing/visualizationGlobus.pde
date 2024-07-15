WavDataExtractor extractor;
FlowField baseFlowField;
FlowField specialFlowField;
Particle[] baseParticles;
Particle[] specialParticles;
int storyCounter = 0;
int totalStories = 0;
int noOfPoints = 6000; // Number of particles
color col;
int storyToDelete = 0;


void setup() {
  // Initialize the SocketListener with a specific port, for example, 12345
  socketListener = new SocketListener(56789);
  // Start the socket listener in a new thread
  socketListener.start();
  size(1280, 1080);
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
  // Socketsays lässt sich mit einem PythonSkript überschreiben so können wir das script stoppen 
  if (socketListener.socketSays == false){
    
    println("Stopping the Audio"); 
    if (extractor != null) {
      extractor.stopAudio(); // Stop the audio playback if any is played
      extractor.close();
      deleteAllFilesInFolder("data");
      storyCounter = 0;
      storyToDelete = 0;
      
    }
    println("Switching to baseShow");
    baseShow();
    println("Deleting all Files");
    deleteAllFilesInFolder("data");
    println("Reseting StoryCounter");
    storyCounter = 0;
  }
  if (extractor == null || !extractor.player.isPlaying()) {
    println("Socket says ", socketListener.socketSays);
    baseShow();
  } else {
    println("Socket says ", socketListener.socketSays);
    specialShow();
  }
}

void draw() {
  showManager();
  countWavFiles();
  if (totalStories > 0) {
    //println("totalStories > 0: " + totalStories);
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
      if (file.isFile() && file.getName().toLowerCase().endsWith(".wav")) {
        count++;
      }

      if (storyCounter > 0 && file.getName().equalsIgnoreCase("story0.wav") && extractor == null) {
        println("Found story0.wav");
        storyCounter = 0;
      }
    }
  }

  totalStories = count;
  //println("Counted files: " + totalStories);
}

// Method to delete all files inside a folder
void deleteAllFilesInFolder(String folderPath) {
  File folder = new File(sketchPath(folderPath));
  File[] files = folder.listFiles();
  
  if (files != null) { // Ensure files is not null
    for (File file : files) {
      if (file.isFile()) {
        if (file.delete()) {
          println("Deleted file: " + file.getName());
        } else {
          println("Failed to delete file: " + file.getName());
        }
      }
    }
  }
}

void playNextStory() {
  println("StoryCounter before playNextStory; ", storyCounter);
  
  if (!isFileInFolder(storyCounter)) {
    println("File not found for storyCounter: " + storyCounter);
    deleteAllFilesInFolder("data");
    extractor.close();
    storyCounter = 0;
    storyToDelete = 0;
    return; // Skip the rest of the method if the file is not found
  }
  
  if (extractor != null) {
    extractor.close();
  }
  
  if (storyToDelete > 0) {
    deleteFile(storyToDelete);
  }
  
  String filePath = String.format("data/story%d.wav", storyCounter);
  extractor = new WavDataExtractor(this, filePath);

  // Call showManager before playing the next story
  showManager();
  println("Playing story part; ", storyCounter);
  extractor.player.play();
  storyToDelete = storyCounter;
  storyCounter++;
  println("StoryCounter after playNextStory; ", storyCounter);
}

void deleteFile(int storyToDelete) {
  // Construct the file path
  println("DeleteFIle called with; ", storyToDelete);
  String filePath = String.format("data/story%d.wav", storyToDelete - 1);
  File fileToDelete = new File(sketchPath(filePath));
  
  // Ensure the file is closed before deleting
  if (extractor != null) {
    extractor.close();
  }

  // Attempt to delete the file
  if (fileToDelete.exists() && fileToDelete.delete()) {
    println("Deleted file: " + filePath);
  } else {
    println("Failed to delete file: " + filePath);
  }
}

boolean isFileInFolder(int count) {
  String filePath = sketchPath(String.format("data/story%d.wav", count));
  println("Checking for File: ", filePath);
  File file = new File(filePath);
  return file.exists();
}
