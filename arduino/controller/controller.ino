

// Electrode 1
int pin_electrode_1_polarity = 2;
int pin_electrode_1_current = 9; // Needs to be a PWM pin to be able to control motor speed

// Electrode 2
int pin_electrode_2_polarity = 4;
int pin_electrode_2_current = 10; // Needs to be a PWM pin to be able to control motor speed


void setup() {
  // initialize serial communication @ 9600 baud:
  Serial.begin(9600);

  //Define L298N Dual H-Bridge Motor Controller Pins

  pinMode(pin_electrode_1_polarity,OUTPUT);
  pinMode(pin_electrode_1_current,OUTPUT);
  pinMode(pin_electrode_2_polarity,OUTPUT);
  pinMode(pin_electrode_2_current,OUTPUT);

  analogWrite(pin_electrode_1_current,0);
  analogWrite(pin_electrode_2_current,0);
  digitalWrite(pin_electrode_1_polarity,LOW);
  digitalWrite(pin_electrode_2_polarity,LOW);
}

void loop() {
  int electrode_1_polarity = LOW;
  int electrode_2_polarity = LOW;
  
  int electrode_1_current = 0;
  int electrode_2_current = 0;
  
  if (Serial.available() > 0) {

  }
  //write currents
  analogWrite(pin_electrode_1_current,electrode_1_current);
  analogWrite(pin_electrode_2_current,electrode_2_current);
  //write polarities
  digitalWrite(pin_electrode_1_polarity,electrode_1_polarity);
  digitalWrite(pin_electrode_2_polarity,electrode_2_polarity);
  //wait
  delay(100);
  
  

}
