#define SAMPLE_SIZE  3
#define potPin 0
int val;

void setup() {
  pinMode(8,OUTPUT);
  digitalWrite(8,HIGH);
  Serial.begin(9600);
}

void loop() {
    val = analogRead(potPin);
    Serial.println(val);
    delay(100);
}


