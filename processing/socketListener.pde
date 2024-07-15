import java.net.*;
import java.io.*;

SocketListener socketListener;

class SocketListener extends Thread {
  ServerSocket server;
  boolean socketSays;

  SocketListener(int port) {
    try {
      server = new ServerSocket(port);
    } catch (IOException e) {
      e.printStackTrace();
    }
  }

  public void run() {
    while (true) {
      try {
        Socket client = server.accept();
        BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
        String line;
        while ((line = in.readLine()) != null) {
          if (line.equals("true")) {
            socketSays = true;
          } else if (line.equals("false")) {
            socketSays = false;
          }
        }
        client.close();
      } catch (IOException e) {
        e.printStackTrace();
      }
    }
  }
}
