class FlowField {
  float inc = 0.05; // Smoothness of direction changes
  int scl;
  float zoff = 0;
  int cols, rows;
  PVector[] flowField;
  
  FlowField(int scale) {
    this.scl = scale;
    this.cols = floor(width / scl);
    this.rows = floor(height / scl);
    this.flowField = new PVector[cols * rows];
  }
  
  void update() {
    float yoff = 0;
    for (int y = 0; y < rows; y++) {
      float xoff = 0;
      for (int x = 0; x < cols; x++) {
        int index = x + y * cols;
        float angle = noise(xoff, yoff, zoff) * TWO_PI;
        PVector v = PVector.fromAngle(angle);
        v.setMag(1); // Set a constant magnitude
        flowField[index] = v;
        xoff += inc;
      }
      yoff += inc;
    }
    zoff += (inc / 20); // Speed of evolution
  }
  
  PVector lookup(PVector lookup) {
    int column = floor(lookup.x / scl);
    int row = floor(lookup.y / scl);
    int index = column + row * cols;
    if (index < flowField.length) {
      return flowField[index].copy();
    } else {
      return new PVector(0, 0);
    }
  }
}
