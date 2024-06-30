class Particle {
  PVector pos;
  PVector vel;
  PVector acc;
  float maxSpeed = 1; // Speed of particles
  PVector prevPos;
  int col;

  Particle(int col) {
    pos = new PVector(random(width), random(height));
    vel = new PVector(0, 0);
    acc = new PVector(0, 0);
    prevPos = pos.copy();
    this.col = col; // Color of particles
  }

  void setColor(int col) {
    this.col = col;
  }

  void update() {
    vel.add(acc);
    vel.limit(maxSpeed);
    pos.add(vel);
    acc.mult(0);
  }

  void follow(PVector force) {
    applyForce(force);
  }

  void applyForce(PVector force) {
    acc.add(force.mult(3)); // Strength of the force
  }

  void show() {
    stroke(col, 50); // Use the particle's color
    strokeWeight(3); // Size of particles
    point(pos.x, pos.y);
  }

  void edges() {
    if (pos.x > width) {
      pos.x = 0;
      updatePrev();
    }
    if (pos.x < 0) {
      pos.x = width;
      updatePrev();
    }

    if (pos.y > height) {
      pos.y = 0;
      updatePrev();
    }
    if (pos.y < 0) {
      pos.y = height;
      updatePrev();
    }
  }

  void updatePrev() {
    prevPos.x = pos.x;
    prevPos.y = pos.y;
  }
}
