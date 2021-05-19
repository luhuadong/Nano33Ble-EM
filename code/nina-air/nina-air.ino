/*
 * Funpack 第八期
 *
 * 功能：读取板载传感器数据，并通过蓝牙BLE发送到客户端显示
 */

#include <ArduinoBLE.h>
#include <Arduino_HTS221.h>
#include <Arduino_LPS22HB.h>
#include <Arduino_APDS9960.h>
#include <PDM.h>

static const char *greeting = "Funpack";

BLEService greetingService("180C"); // User defined service

// standard 16-bit characteristic UUID
// remote clients will only be able to read this
BLEStringCharacteristic greetingCharacteristic("2A56", BLERead, 13);

const float CALIBRATION_FACTOR = -4.0; // Temperature calibration factor (Celsius)

int previousTemperature = 0;
unsigned int previousHumidity = 0;
unsigned int previousPressure = 0;
unsigned int previousLight    = 0;
unsigned int previousNoise    = 0;

#define UUID_ENV_SENSING_SERVICE   "181A"
#define UUID_PRESSURE_CHAR         "2A6D"
#define UUID_TEMPERATURE_CHAR      "2A6E"
#define UUID_HUMIDITY_CHAR         "2A6F"
#define UUID_LIGHT_CHAR            "936b6a25-e503-4f7c-9349-bcc76c22b8c3"
#define UUID_NOISE_CHAR            "936b6a25-e503-4f7c-9349-bcc76c22b8c4"


BLEService environmentService("181A"); // Standard Environmental Sensing service

/* Temperature characteristic  16-bit
 * Humidity characteristic     Unsigned 16-bit
 * Pressure characteristic     Unsigned 32-bit
 * 
 * Flag: Remote clients can read and get updates
*/
BLEIntCharacteristic tempCharacteristic("2A6E", BLERead | BLENotify);
BLEUnsignedIntCharacteristic humidCharacteristic("2A6F", BLERead | BLENotify);
BLEUnsignedIntCharacteristic pressureCharacteristic("2A6D", BLERead | BLENotify);

BLEUnsignedIntCharacteristic lightCharacteristic(UUID_LIGHT_CHAR, BLERead | BLENotify);
BLEUnsignedIntCharacteristic noiseCharacteristic(UUID_NOISE_CHAR, BLERead | BLENotify);

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

    // initialize BLE
    if (!BLE.begin()) { 
        Serial.println("starting BLE failed!");
        while (1);
    }
    
    // Set name for connection
    BLE.setLocalName("Nano33BLE");

    // greetingService
    BLE.setAdvertisedService(greetingService);                 // Advertise service
    greetingService.addCharacteristic(greetingCharacteristic); // Add characteristic to service
    BLE.addService(greetingService);                           // Add service
    greetingCharacteristic.setValue(greeting);                 // Set greeting string
    
    // environmentService
    BLE.setAdvertisedService(environmentService); // Advertise environment service

    environmentService.addCharacteristic(tempCharacteristic);     // Add temperature characteristic
    environmentService.addCharacteristic(humidCharacteristic);    // Add humidity characteristic
    environmentService.addCharacteristic(pressureCharacteristic); // Add pressure characteristic
    environmentService.addCharacteristic(lightCharacteristic);    // Add light characteristic
    environmentService.addCharacteristic(noiseCharacteristic);    // Add noise characteristic

    BLE.addService(environmentService); // Add environment service

    tempCharacteristic.setValue(0);     // Set initial temperature value
    humidCharacteristic.setValue(0);    // Set initial humidity value
    pressureCharacteristic.setValue(0); // Set initial pressure value
    lightCharacteristic.setValue(0);    // set initial light value
    noiseCharacteristic.setValue(0);    // set initial noise value

    // Start advertising
    BLE.advertise();
    Serial.print("Peripheral device MAC: ");
    Serial.println(BLE.address());
    Serial.println("Waiting for connections...");
}

void loop() 
{
    BLEDevice central = BLE.central(); // Wait for a BLE central to connect
    
    // if a central is connected to the peripheral:
    if (central)
    {
        Serial.print("Connected to central MAC: ");
        // print the central's BT address:
        Serial.println(central.address());
        // turn on the LED to indicate the connection:
        digitalWrite(LED_BUILTIN, HIGH);
        
        while (central.connected())
        {
            updateReadings();
            delay(1000);
        } // keep looping while connected
        
        // when the central disconnects, turn off the LED:
        digitalWrite(LED_BUILTIN, LOW);
        Serial.print("Disconnected from central MAC: ");
        Serial.println(central.address());
    }
}

void updateReadings() 
{
    int temperature = getTemperature(CALIBRATION_FACTOR);
    unsigned int humidity = getHumidity();
    unsigned int pressure = getPressure();
    unsigned int light    = getLight();
    unsigned int noise    = getNoise();

    if (temperature != previousTemperature) { // If reading has changed
        tempCharacteristic.writeValue(temperature); // Update characteristic
        previousTemperature = temperature;          // Save value
    }

    if (humidity != previousHumidity) { // If reading has changed
        humidCharacteristic.writeValue(humidity);
        previousHumidity = humidity;
    }

    if (pressure != previousPressure) { // If reading has changed
        pressureCharacteristic.writeValue(pressure);
        previousPressure = pressure;
    }

    if (light != previousLight) { // If reading has changed
        lightCharacteristic.writeValue(light);
        previousLight = light;
    }

    if (noise != previousNoise) { // If reading has changed
        noiseCharacteristic.writeValue(noise);
        previousNoise = noise;
    }

    Serial.println("--------------------------------");
}

// Get calibrated temperature as signed 16-bit int for BLE characteristic
int getTemperature(float calibration) 
{
    float temperature = HTS.readTemperature();

    Serial.print("Temperature = ");
    Serial.print(temperature);
    Serial.println(" °C");

    return (int)((temperature + calibration) * 100);
}

// Get humidity as unsigned 16-bit int for BLE characteristic
unsigned int getHumidity() 
{
    float humidity = HTS.readHumidity();

    Serial.print("Humidity    = ");
    Serial.print(humidity);
    Serial.println(" %");

    return (unsigned int)(humidity * 100);
}

// Get humidity as unsigned 32-bit int for BLE characteristic
unsigned int getPressure() 
{
    float pressure = BARO.readPressure();

    Serial.print("Pressure    = ");
    Serial.print(pressure);
    Serial.println(" kPa");

    return (unsigned int)(pressure * 1000 * 10);
}

// get ambience illumination sensor
unsigned int getLight()
{
    while (! APDS.colorAvailable()) {
        delay(5);
    }
    int r, g, b;
    APDS.readColor(r, g, b);
    float gray = float(r+g+b)/122.91;

    // print the sensor value
    Serial.print("Gray        = ");
    Serial.print(gray);
    if (gray < 0.5) {
        Serial.println(" (Night)");
    }
    else {
        Serial.println(" (Day)");
    }

    return (unsigned int)(gray * 100);
}

// get digital microphone sensor
unsigned int getNoise()
{
    // sound
    double spl = SPL_cal();

    // print the sensor value
    Serial.print("Noise       = ");
    Serial.print(spl);
    Serial.println(" dB");

    return (unsigned int)(spl * 100);
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
