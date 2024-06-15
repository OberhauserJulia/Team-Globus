import ddf.minim.*;
import ddf.minim.analysis.*;
import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.util.ArrayList;
import java.util.Iterator;

Minim minim;
AudioPlayer player;
FFT fft;
ArrayList<Bubble> bubbles;
int timeToLive = 3000; // Zeit in Millisekunden (3 Sekunden)
boolean captureText = true;
boolean colorChange = false; // Variable, um den Zustand der Farbänderung zu speichern
int bandsize = 1;
int r = 0;
int g = 0;
int b = 0;
int picturecount = 0;
TextUI textUI;
HttpServer server;

void setup() {
  size(800, 600, P2D);
  minim = new Minim(this);
  player = minim.loadFile("song.mp3");
  player.play();
  fft = new FFT(player.bufferSize(), player.sampleRate());
  bubbles = new ArrayList<Bubble>();
  textUI = new TextUI(0, 0, 0); // Initialisiere die TextUI mit den Startfarben

  // Setup HTTP server
  try {
    server = HttpServer.create(new InetSocketAddress("127.0.0.1", 5204), 0);
    server.createContext("/setRGB", new RGBHandler());
    server.createContext("/setBandsize", new BandsizeHandler());
    server.setExecutor(null); // creates a default executor
    server.start();
    println("Server started on port 5204");
  } catch (IOException e) {
    e.printStackTrace();
  }
}

void draw() {
  background(0);

  if (captureText && textUI != null) {
    textUI.display(50, 100);
  }

  // Analyse der Frequenzen
  fft.forward(player.mix);

  // Aktualisieren und Zeichnen aller Kreise (Bubbles)
  Iterator<Bubble> bubbleIterator = bubbles.iterator();
  while (bubbleIterator.hasNext()) {
    Bubble bubble = bubbleIterator.next();
    bubble.update();
    bubble.display();
    if (bubble.isDead()) {
      bubbleIterator.remove();
    }
  }

  // Visualisierung der Bassfrequenzen
  strokeWeight(5);
  for (int i = 0; i < fft.specSize(); i++) {
    float band = fft.getBand(i);
    float ciclesize = Math.abs(bandsize * band);
    textSize(32); // Textgröße festlegen
    fill(255); // Textfarbe auf Weiß setzen
    text(str(ciclesize) + 10, 50, 50); // Text anzeigen
    float yPos = map(band, 0, 100, height, 0);
    if (colorChange) {
      stroke(color(random(255), random(255), random(255)), 100);
    } else {
      stroke(255, 100); // Standardfarbe für die Linien
    }
    float xPos = i * (width / (float)fft.specSize()); // Skaliere die x-Position auf die Bildschirmbreite
    line(width/2 - xPos, height, width/2 - xPos, yPos); // Spiegle die x-Position um die Mitte des Bildschirms
    line(width/2 + xPos, height, width/2 + xPos, yPos); // Spiegle die x-Position um die Mitte des Bildschirms
    if (i < 20) { // Prüfe, ob wir uns in der "Basszone" befinden
      if (colorChange) {
        // Hinzufügen eines Kreises basierend auf einer der Bassfrequenzen mit schwarz-weißer Farbe
        bubbles.add(new Bubble(random(width), random(height), ciclesize, color(r, g, b), ciclesize));
      } else {
        // Hinzufügen eines Kreises basierend auf einer der Bassfrequenzen mit zufälliger Farbe
        bubbles.add(new Bubble(random(width), random(height), ciclesize, color(random(255), random(255), random(255)), ciclesize));
      }
    }
  }
}

// Input Map:
void keyPressed() {
  if (key == ' ') {
    colorChange = !colorChange; // Ändert den Zustand der Farbänderung, wenn die Leertaste gedrückt wird
  } else if (key == 'a') {
    bandsize += 1;
  } else if (key == 'd') {
    bandsize -= 1;
  } else if (key == 'r') {
    r -= 10;
    textUI.setR(10);
  } else if (key == 'g') {
    g -= 10;
    textUI.setG(10);
  } else if (key == 'b') {
    b -= 10;
    textUI.setB(10);
  } else if (key == 'w') {
    textUI.setWhite();
    r = 255;
    g = 255;
    b = 255;
  } else if (key == 't') {
    // Umschalten der captureText-Variable beim Drücken der Taste 't'
    captureText = !captureText;
  } else if (key == 's') {
    // Temporär das Textobjekt deaktivieren
    boolean originalCaptureText = captureText;
    captureText = false;
    // Speichern des Screenshots ohne Text
    saveFrame(str(picturecount) + "screenshot.png");
    // Textobjekt wieder aktivieren
    captureText = originalCaptureText;
    picturecount += 1;
  }
}

void stop() {
  player.close();
  minim.stop();
  server.stop(0);
  super.stop();
}

// HTTP Handler for setting RGB values
class RGBHandler implements HttpHandler {
  @Override
  public void handle(HttpExchange t) throws IOException {
    String query = t.getRequestURI().getQuery();
    String[] params = query.split("&");
    for (String param : params) {
      String[] pair = param.split("=");
      if (pair[0].equals("r")) {
        r = Integer.parseInt(pair[1]);
      } else if (pair[0].equals("g")) {
        g = Integer.parseInt(pair[1]);
      } else if (pair[0].equals("b")) {
        b = Integer.parseInt(pair[1]);
      }
    }
    String response = "RGB values set to - R: " + r + ", G: " + g + ", B: " + b;
    t.sendResponseHeaders(200, response.length());
    OutputStream os = t.getResponseBody();
    os.write(response.getBytes());
    os.close();
  }
}

// HTTP Handler for setting bandsize
class BandsizeHandler implements HttpHandler {
  @Override
  public void handle(HttpExchange t) throws IOException {
    String query = t.getRequestURI().getQuery();
    String[] params = query.split("&");
    for (String param : params) {
      String[] pair = param.split("=");
      if (pair[0].equals("bandsize")) {
        int newBandsize = Integer.parseInt(pair[1]);
        bandsize = newBandsize;
      }
    }
    String response = "Bandsize set to " + bandsize;
    t.sendResponseHeaders(200, response.length());
    OutputStream os = t.getResponseBody();
    os.write(response.getBytes());
    os.close();
  }
}
