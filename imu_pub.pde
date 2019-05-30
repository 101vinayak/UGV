#include <ros.h>
#include <std_msgs/String.h>
 
const int MPU_addr=0x68;  // I2C address of the MPU-6050
int16_t AcX,AcY,AcZ,Tmp,GyX,GyY,GyZ;
 
 
//Set up the ros node and publisher
std_msgs::String imu_msg;
ros::Publisher imu("imu", &imu_msg);
ros::NodeHandle nh;
 
 
                           
void setup()
{
 
  nh.initNode();
  nh.advertise(imu);
  
  Serial.begin(9600);
}
 
long publisher_timer;
 
void loop()
{
  String AX = String(AcX);
  String AY = String(AcY);
  String AZ = String(AcZ);
  String GX = String(GyX);
  String GY = String(GyY);
  String GZ = String(GyZ);
  String tmp = String(Tmp);
 
  String data = "A" + AX + "B"+ AY + "C" + AZ + "D" + GX + "E" + GY + "F" + GZ + "G" ;
  Serial.println(data);
  int length = data.indexOf("G") +2;
  char data_final[length+1];
  data.toCharArray(data_final, length+1);
  
  if (millis() > publisher_timer) {
    // step 1: request reading from sensor
    imu_msg.data = data_final;
    imu.publish(&imu_msg);
    publisher_timer = millis() + 100; //publish ten times a second
    nh.spinOnce();
  }  
}
