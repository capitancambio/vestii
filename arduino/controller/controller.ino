#include <Arduino.h>


// Electrode 1

int pin_electrode_1_current = 10; // Needs to be a PWM pin to be able to control motor speed
int pin_electrode_1_polarity_A = 9;
int pin_electrode_1_polarity_B = 8;
// Electrode 2
int pin_electrode_2_polarity_A = 7;
int pin_electrode_2_polarity_B = 6;
int pin_electrode_2_current = 5; // Needs to be a PWM pin to be able to control motor speed

String InBuffer;
String Sub2;
int CharNum2;
String Sub3;

void setup() {
  // initialize serial communication @ 9600 baud:
  Serial.begin(9600);

  //Define L298N Dual H-Bridge Motor Controller Pins

  pinMode(pin_electrode_1_polarity_A,OUTPUT);
  pinMode(pin_electrode_1_polarity_B,OUTPUT);
  pinMode(pin_electrode_1_current,OUTPUT);

  pinMode(pin_electrode_2_polarity_A,OUTPUT);
  pinMode(pin_electrode_2_polarity_B,OUTPUT);
  pinMode(pin_electrode_2_current,OUTPUT);

  analogWrite(pin_electrode_1_current,0);
  analogWrite(pin_electrode_2_current,0);
  digitalWrite(pin_electrode_1_polarity_A,LOW);
  digitalWrite(pin_electrode_1_polarity_B,HIGH);

  digitalWrite(pin_electrode_2_polarity_A,LOW);
  digitalWrite(pin_electrode_2_polarity_B,HIGH);

}

void loop() {
  //allowed values are 0 or 1 for polarity
  int electrode_1_polarity = 0;
  int electrode_2_polarity = 0;

  int electrode_1_current = 0;
  int electrode_2_current = 0;


  while (Serial.available() > 0)  // While there is something in the Serial buffer
    {

      char Incoming = Serial.read();
      InBuffer += Incoming;  // Concatonates individual characters from buffer into meaningful string

      if(Incoming == '\n') {  // Signifies end of stream from Python

        char ElecNum = InBuffer.charAt(0);   //Useful definitions  //ElecNum is the set number of electrodes
        String StorageArray[ElecNum];
        int CurArray[ElecNum];
        int PolArray[ElecNum];

        InBuffer = InBuffer.substring(1);  // Removes the char indicating number of electrodes
        int CharNum;

        for(int x=0; x<ElecNum; x++) {  // Splits input string into individual electrodes
           CharNum = InBuffer.indexOf('$');
           StorageArray[x] = InBuffer.substring(0, (CharNum + 1));
           InBuffer = InBuffer.substring(CharNum + 1);
        }



        for(int x=0; x<ElecNum; x++) {  // Retrieves both current and polarity values from electrode strings

        CharNum = StorageArray[x].indexOf('#');
        CurArray[x] = (StorageArray[x].substring(0, CharNum)).toInt();
        Sub2 = InBuffer.substring((CharNum + 1));
        CharNum2 = Sub2.indexOf('$');
        Sub3 = Sub2.substring(0,CharNum2);
        PolArray[x] = (Sub3.toInt());

        }
        electrode_1_current = CurArray[0];  // This part is not robust, will be a for loop.
        electrode_2_current = CurArray[1];  // Need to figure out how to dynamically declare variables
        electrode_1_polarity = PolArray[0];
        electrode_2_polarity = PolArray[1];

        InBuffer = ""; // This resets the buffer
          }}


  //write currents



  analogWrite(pin_electrode_1_current,electrode_1_current);
  analogWrite(pin_electrode_2_current,electrode_2_current);
  //write polarities
  if (electrode_1_polarity == 0){
    digitalWrite(pin_electrode_1_polarity_A,LOW);
    digitalWrite(pin_electrode_1_polarity_B,HIGH);
  }else{
    digitalWrite(pin_electrode_1_polarity_A,HIGH);
    digitalWrite(pin_electrode_1_polarity_B,LOW);
  }

  if (electrode_2_polarity == 0){
    digitalWrite(pin_electrode_2_polarity_A,LOW);
    digitalWrite(pin_electrode_2_polarity_B,HIGH);
  }else{
    digitalWrite(pin_electrode_2_polarity_A,HIGH);
    digitalWrite(pin_electrode_2_polarity_B,LOW);
  }
  //wait
  delay(100);



}
