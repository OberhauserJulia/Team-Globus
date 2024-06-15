class TextUI {
  int r, g, b;
  
  TextUI(int r, int g, int b) {
    this.r = r;
    this.g = g;
    this.b = b;
  }
 void setR(int newR) {
  this.r -= newR; 
}
void setG(int newG) {
  this.g -= newG; 
}

void setB(int newB) {
  this.b -= newB; 
}
void setWhite() {
  this.r = 255; 
  this.g = 255 ; 
  this.b = 255 ; 
}


  
  void display(int x, int y) {
    textSize(32);
    fill(255);
    text("Color Controls", x, y+10 );
   
  
    
    
fill(255);
    textSize(16);
    text("R: " + r, x, y + 30);
    text("G: " + g, x, y + 70);
    text("B: " + b, x, y + 110);
    
    
    text("Press 'w' for white bubbles", x, y + 160);
    text("Press 'd' to increase sensitivity", x, y + 190);
    text("Press 'a' to decrease sensitivity", x, y + 220);
    text("Press 't' to toggle the UI", x, y + 250);
    text("Press Space to activate/deactivate random mode", x, y + 280);
  }
}
