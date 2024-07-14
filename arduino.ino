#include <Servo.h>

Servo servo; // Declare Servo object

int x;
int r;
int PWM = 5; // PWM, INA, INB are for the rear motor controller
int INA = 8;
int INB = 7;
int servo_pin = 9; // Servo pin (9 or 10 pins are supported)

void setup() {
  Serial.begin(9600);
  servo.attach(servo_pin); // Attach servo to pin 9
  servo.write(90); // Center the servo (adjust as needed)
  pinMode(PWM, OUTPUT);
  pinMode(INA, OUTPUT);
  pinMode(INB, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    if (Serial.read() == 'R') {
      r = Serial.parseInt();
      if (Serial.read() == 'X') {
        x = Serial.parseInt();
        Serial.print(r);
        Serial.print(" ");
        Serial.print(x);
        Serial.println();
        if (r < 0) {
          analogWrite(PWM, 200);  // Control speed (replace 150 with r if needed)
          digitalWrite(INA, LOW); // Set motor direction
          digitalWrite(INB, HIGH); 
        } else if (r>0) {
          analogWrite(PWM, 200); // Control speed (replace 150 with -r if needed)
          digitalWrite(INA, HIGH); // Set motor direction (reverse if needed)
          digitalWrite(INB, LOW); 
        }
          else {
            analogWrite(PWM, 200); // Control speed (replace 150 with -r if needed)
          digitalWrite(INA, LOW); // Set motor direction (reverse if needed)
          digitalWrite(INB, LOW);
          }
        servo.write(x); // Move servo to desired position
      }
    }
  }
}