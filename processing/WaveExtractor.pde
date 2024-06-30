import ddf.minim.*;
import ddf.minim.analysis.*;

class WavDataExtractor {
  Minim minim;
  AudioPlayer player;
  AudioBuffer leftBuffer;
  AudioBuffer rightBuffer;
  FFT fft;
  int bufferSize;
  float[] leftChannelData;
  float[] rightChannelData;
  float[] frequencyData;

  WavDataExtractor(PApplet app, String filePath) {
    minim = new Minim(app);
    String fullPath = app.sketchPath(filePath);
    player = minim.loadFile(fullPath);
    bufferSize = player.bufferSize();
    leftBuffer = player.left;
    rightBuffer = player.right;
    fft = new FFT(bufferSize, player.sampleRate());
    leftChannelData = new float[bufferSize];
    rightChannelData = new float[bufferSize];
    frequencyData = new float[bufferSize/2];
  }

  void update() {
    // Update left and right channel data
    for (int i = 0; i < bufferSize; i++) {
      leftChannelData[i] = leftBuffer.get(i);
      rightChannelData[i] = rightBuffer.get(i);
    }
    // Update FFT frequency data
    fft.forward(player.mix);
    for (int i = 0; i < frequencyData.length; i++) {
      frequencyData[i] = fft.getBand(i);
    }
  }

  float[] getLeftChannelData() {
    return leftChannelData;
  }

  float[] getRightChannelData() {
    return rightChannelData;
  }

  float[] getFrequencyData() {
    return frequencyData;
  }

  void close() {
    player.close();
    minim.stop();
  }
}
