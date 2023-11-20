//
//  Doll.cpp
//  FinalAssignment
//
//  Created by Muyang Eric Huang on 2020/07/16.
//

#include "ofMain.h"
#include "Doll.h"

////  constructor.
//dools::dolls(){
//    setup();
//}

//--------------------------------------------------------------
void Doll::setup () {
    //  init with default values
    posX = 0; posY = 0; scaleXY = 1;
    colorR = ofRandom(250);
    colorG = ofRandom(250);
    colorB = ofRandom(250);
    period = 1000; range = 30;
    radius = 0;
    LLeg = RLeg = 0;
    LArm = RArm = 0;
    BodyM = 0;
    
//    i = 1;
}

//--------------------------------------------------------------
void Doll::update () {
    //  update posture
    float s = sin(radius);
    LLeg = 30 + range * s;
    RLeg = 30 - range * s;
    LArm = 30 - range * s;
    RArm = 30 + range * s;
    BodyM = 15 * sin(radius * 2 - HALF_PI);
    //  increment the phase
    radius += 0.5 * 1000 / period * TWO_PI / 30;
}

//--------------------------------------------------------------
void Doll::draw () {
//    //  setup standard coordinate system.
//    ofTranslate(ofGetWindowWidth()/2, ofGetWindowHeight()/2);
//    ofScale(1, -1);
    
    //  encapsulation.
    ofPushMatrix();
    ofPushStyle();
    ofSetCircleResolution(32);
    ofSetRectMode(OF_RECTMODE_CENTER);
    //  position/scale.
    ofTranslate(posX, posY);
    ofScale(scaleXY, scaleXY);
    //  color.
    ofSetColor(ofRandom(250), ofRandom(250), ofRandom(250));
    
    //  body.
    ofTranslate(0, BodyM);
    ofDrawRectangle(0, 0, 50, 80);
    //  head.
    ofPushMatrix();
    ofTranslate(0, BodyM);
    ofDrawCircle(0, 80, 30);
    ofPopMatrix();
    
    //  left leg.
    ofPushMatrix();
    ofTranslate(-10, -45);
    ofRotateZDeg(-(30 + LLeg));
    ofTranslate(0, -35);
    ofDrawRectangle(0, -35, 20, 50);
    ofTranslate(0, -70);
    ofRotateZDeg(60-100*i);
    ofTranslate(0, -35);
    ofDrawRectangle(0, -35, 20, 50);
    ofPopMatrix();
    //  right leg.
    ofPushMatrix();
    ofTranslate(10, -45);
    ofRotateZDeg(30 + RLeg);
    ofTranslate(0, -35);
    ofDrawRectangle(0, 0, 20, 50);
    ofTranslate(0, -35);
    ofRotateZDeg(-(60 + RLeg));
    ofTranslate(0, -35);
    ofDrawRectangle(0, 0, 20, 50);
    ofPopMatrix();
    //  left arm.
    ofPushMatrix();
    ofTranslate(-35, 40);
    ofRotateZDeg(-(30 + LArm));
    ofTranslate(0, -30);
    ofDrawRectangle(0, -30, 20, 45);
    ofTranslate(0, -60);
    ofRotateZDeg(-(60+5*i));
    ofTranslate(0, -30);
    ofDrawRectangle(0, -30, 20, 45);
    ofPopMatrix();
    //  right arm.
    ofPushMatrix();
    ofTranslate(35, 40);
    ofRotateZDeg(30 + RArm);
    ofTranslate(0, -30);
    ofDrawRectangle(0, -30, 20, 45);
    ofTranslate(0, -60);
    ofRotateZDeg(60+10*i);
    ofTranslate(0, -30);
    ofDrawRectangle(0, -30, 20, 45);
    ofPopMatrix();
    
    //  face.
    ofPushMatrix();
    ofSetColor(0);
    ofTranslate(0, BodyM-5);
    ofDrawCircle(-1, 80, 10);
    ofTranslate(0, BodyM+5);
    ofDrawCircle(1, 80, 10);
    ofPopMatrix();
    
    //  restoration.
    ofPopStyle();
    ofPopMatrix();
    
    i++;
    
    ofSetColor(125-125*sin(i), 125-125*sin(i), 125-125*sin(i));
    ofDrawBitmapString("The Doll.", 100, 300);
//    ofDrawBitmapString("Please Press the Space Key.", 100, 260);
}

//--------------------------------------------------------------
void Doll::setColor (int r, int g, int b) {
    //  set skin color.
    colorR = r; colorG = g; colorB = b;
}

//--------------------------------------------------------------
void Doll::setPosition (float x, float y) {
    //  set position (0, 0).
    posX = x; posY = y;
}

//--------------------------------------------------------------
void Doll::setScale (float scale) {
    //  set scale (1).
    scaleXY = scale;
}

//--------------------------------------------------------------
void Doll::setPeriod (float msec) {
    //  set period (1000).
    period = msec;
}

//--------------------------------------------------------------
void Doll::setRange (float deg) {
    //  set range of motion (30).
    range = deg;
}
