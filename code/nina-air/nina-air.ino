/*
  读取板载 HTS221 传感器数据，并每秒打印一次温度和湿度值到监视器
*/

#include <Arduino_HTS221.h>
#include <Arduino_LPS22HB.h>
#include <Arduino_APDS9960.h>
#include <PDM.h>

// SPL calculation variables
static const char channels = 1;  // default number of output channels
static const int frequency = 16000;  // default PCM output frequency
short sampleBuffer[512];   // Buffer to read samples into, each sample is 16bits
volatile int samplesRead;  // Number of audio samples read

void setup() 
{
    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, HIGH);
  
    Serial.begin(9600);
    while (!Serial);

    if (!HTS.begin()) {
        Serial.println("Failed to initialize humidity temperature sensor!");
        while (1);
    }

    if (!BARO.begin()) {
        Serial.println("Failed to initialize pressure sensor!");
        while (1);
    }

    if (!APDS.begin()) {
        Serial.println("Error initializing APDS9960 sensor.");
    }

    // initialise PDM microphone
    PDM.onReceive(onPDMdata);
    PDM.setGain(20);
    if (!PDM.begin(channels, frequency)) {
        Serial.println("Failed to start PDM!");
        while (1);
    }
}

void loop() 
{
    // read all the sensor values
    float temperature = HTS.readTemperature();
    float humidity    = HTS.readHumidity();

    // read the sensor value
    float pressure = BARO.readPressure();

    // get ambience illumination sensor
    while (! APDS.colorAvailable()) {
        delay(5);
    }
    int r, g, b;
    APDS.readColor(r, g, b);
    float gray = float(r+g+b)/122.91;

    // sound
    double spl = SPL_cal();

    Serial.println("--------------------------------");
    
    // print each of the sensor values
    Serial.print("Temperature = ");
    Serial.print(temperature);
    Serial.println(" °C");

    Serial.print("Humidity    = ");
    Serial.print(humidity);
    Serial.println(" %");

    // print the sensor value
    Serial.print("Pressure    = ");
    Serial.print(pressure);
    Serial.println(" kPa");

    // print the sensor value
    Serial.print("Gray        = ");
    Serial.print(gray);
    if (gray < 0.5) {
        Serial.println(" (Night)");
    }
    else {
        Serial.println(" (Day)");
    }

    // print the sensor value
    Serial.print("Noise       = ");
    Serial.print(spl);
    Serial.println(" dB");

    // print an empty line
    Serial.println();

    // wait 1 second to print again
    delay(1000);

    // blink led
    if (HIGH == digitalRead(LED_BUILTIN)) {
        digitalWrite(LED_BUILTIN, LOW);
    }
    else {
        digitalWrite(LED_BUILTIN, HIGH);
    }
}

void onPDMdata()
{
    int bytesAvailable = PDM.available();
    PDM.read(sampleBuffer, bytesAvailable);
    samplesRead = bytesAvailable / 2;
}

double SPL_cal()
{
    double amp = 0;  // amp: amplitude of sound
    double sum = 0;
    int cnt = 0;     // max: 1023, 15.625Hz
    while (cnt<1020) // 1024
    {
        if (samplesRead)
        {
            for (int i=0; i<samplesRead; i++)
            {
                sum += double(sampleBuffer[i])*sampleBuffer[i];
            }
            cnt += samplesRead;
            samplesRead = 0;
        }
        
        amp = 20 * log10(10*sqrt(sum/cnt));
        return amp;
    }
}
