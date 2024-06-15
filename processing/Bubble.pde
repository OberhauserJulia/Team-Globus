class Bubble {
  float x, y, size, sizey;
  color col;
  int bornTime;
  float alpha; // Transparenz des Kreises
  
  Bubble(float x, float y, float size, color col, float sizey) {
    this.x = x;
    this.y = y;
    this.size = size;
    this.sizey = sizey ; 
    this.col = col;
    bornTime = millis(); // Speichert den Erstellungszeitpunkt
    alpha = 255; // Startet voll sichtbar
  }
  
  void update() {
    // Aktualisiert die Transparenz des Kreises über die Zeit für Fade-Out-Effekt
    int age = millis() - bornTime;
    if (age < timeToLive) {
      alpha = map(age, 0, timeToLive, 255, 0);
      float noiseValue = noise(x * 0.01, y * 0.01, frameCount * 0.01); // Perlin-Noise basierend auf x, y und frameCount
      if (this.size < 1) {
      this.size = map(noiseValue, 0, 0.5, size - 5, size + 5); // Ändere size basierend auf Perlin-Noise
      this.sizey = map(noiseValue, 0,0.5, sizey - 5, sizey + 5); // Ändere sizey basierend auf Perlin-Noise
       }
     if (this.size> 300) {
       this.size = map(noiseValue, 0, 1, size - 5, size + 5); // Ändere size basierend auf Perlin-Noise
      this.sizey = map(noiseValue, 0, 1, sizey - 5, sizey + 5); // Ändere sizey basierend auf Perlin-Noise
       
     }
  
} else {
      alpha = 0;
    }
  }
  
  void display() {
    noStroke();
    fill(col, alpha);
    if (this.size < 100) {ellipse(x, y, size, sizey); }
    if (this.size > 300) {ellipse(x, y, size, sizey); }
  }
  
  boolean isDead() {
    return alpha <= 0;
  }
}
