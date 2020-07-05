/**
 * @version v2-sm.ar
 * @LICENSE MIT
 * 
 * im using buttons wired from ground to port in normal close state,
 * when press it interrupts the PULLDOWN and count as pressed.
 * feel free to modify to your usecase
 * 
 * Warning:
 * 	to do PULLUP and count it needs an debounce,
 * 	in this case  not read the pin state for some time
 * 
 * 	this leads to a problem:
 * 	if you keep pressing the button it will send the code
 * 	when debounce delay ends, so there are application you may
 *  cant use with it.
*/


#define LEDI 13  // LED indicator

/** pre define for optional parameters */
void ledOn (int led = LEDI);
void ledOff(int led = LEDI);


int
	killcount = 0,
	debounce = 5,
	killPin = 2, // stop script button
	btns[] = {7,8,9,10, killPin}; // buttons
	

// learn more at https://www.arduino.cc/en/Reference/PortManipulation
// some bords may not support or have different PINB, PIND... (im using UNO)
// PIND: 0~7, PINB: 8~13
bool usePortManipulation = true;


void setup() {
	Serial.begin(115200);

	for(int i = 0; i < sizeof(btns); i++){
		pinMode(btns[i], INPUT_PULLUP);
	}

	pinMode(LEDI, OUTPUT);


	Serial.println("lstart"); 
}


void loop() {
	
  	if(digitalRead(killPin) == HIGH){
		ledOn();
		if(killcount >= 15){
			Serial.println("kil");
			blinkLED(30, 25, LEDI);
			killcount = 0;
			delay(50);
		}

		killcount++;
		delay(200);
	}

	/**
	 * PIND/PINB returns in the digital ports state in binary,
	 * making an OR operation to get the
	 * the result number, it DOES NOT represent
	 * the actual port number
	 * 
	 * probably there is a better way to do this,
	*/

	if(usePortManipulation){
		// using Port manipulation PIND: 0~7, PINB: 8~13
		if((PIND | 0b00000000) == 131){ sendKey("A7"); }
		else if((PINB | 0b00000000) == 1){ sendKey("A8"); }
		else if((PINB | 0b00000000) == 2){ sendKey("A9"); }
		else if((PINB | 0b00000000) == 4){ sendKey("B0"); }
	}
	else {
		// for normal and compatibility usage
		if(digitalRead(7) == HIGH){
			sendKey("A7");
		}
		else if(digitalRead(8) == HIGH){
			sendKey("A8");
		}
		else if(digitalRead(9) == HIGH){
			sendKey("A9");
		}
		else if(digitalRead(10) == HIGH){
			sendKey("B0");
		}
	}

	ledOff();
}

void sendKey(String key){
	// Serial.println((PIND | 0b00000000));
	Serial.println(key);
	ledOn();
	killcount = 0;
	delay(debounce);
}

void ledOn (int led){ digitalWrite(led, HIGH); }
void ledOff(int led){ digitalWrite(led, LOW);  }

void blinkLED(int del, int qtt, int led){
	while (qtt >= 0){
		ledOn(led);
		delay(del);
		ledOff(led);
		delay(del);
		qtt--;
	}
}
