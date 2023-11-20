#include "ofApp.h"

//--------------------------------------------------------------
void ofApp::setup(){
    ofSetBackgroundColor(0); //  black.
    ofSetFrameRate(60); //  一秒に60回中身が呼ばれる．
    ofSetBackgroundAuto(true); //  引数にfalseかtrueがある．
    
    ofSetWindowShape(700, 768);
    ofSetCircleResolution(32);
    ofSetRectMode(OF_RECTMODE_CENTER);
    
//    i = 1;
//    radius = 0;
//    LLeg = RLeg = 0;
//    LArm = RArm = 0;
//    BodyM = 0;
    
    for(int i = 0; i < DOLLS; i++){
        dolls[i].setup();
        dolls[i].setScale(ofRandom(0.1, 0.3));
        dolls[i].setPeriod(ofRandom(300, 900));
        dolls[i].setRange(ofRandom(10, 50));
        dolls[i].setPosition(((ofRandom(DOLLS) / 12) - 5.5) * 48, (((ofRandom(DOLLS) / 12) - 1.5) * 88 ));
    }
}

//--------------------------------------------------------------
void ofApp::update(){
    float s = sin(radius);
    LLeg = 30 + 30 * s;
    RLeg = 30 - 30 * s;
    LArm = 30 - 30 * s;
    RArm = 30 + 30 * s;
    BodyM = 15 * sin(radius * 2 - HALF_PI);
    radius += 0.1;
    
    for(int i = 0; i < DOLLS; i++){
        dolls[i].update();
    }
}

//--------------------------------------------------------------
void ofApp::draw(){
    //  setup standard coordinate system.
    ofTranslate(ofGetWindowWidth()/2, ofGetWindowHeight()/2);
    ofScale(1, -1);
    
    for(int i = 0; i < DOLLS; i++){
        dolls[i].draw();
    }
    
//    //  ground
//    ofSetColor(50, 0, 0);
//    ofBeginShape();
//        ofVertex(-200, -200);
//        ofVertex(-100, -120);
//        ofVertex( 100, -120);
//        ofVertex( 200, -200);
//        ofVertex(-200, -200);
//    ofEndShape();
//    //  color
//    ofSetColor(ofRandom(250), ofRandom(250), ofRandom(250));
//    //  move all up/down
//
//    //  body
//    ofDrawRectangle(0, 0, 50, 80);
//    //  head
//    ofPushMatrix();
//        ofTranslate(0, movBody);
//        ofDrawCircle(0, 80, 30);
//    ofPopMatrix();
//    //  left leg (upper/lower)
//    ofPushMatrix();
//        ofTranslate(-10, -45);
//        ofRotateZDeg(-(30 + degLLeg));
//        ofDrawRectangle(0, -35, 20, 50);
//        ofTranslate(0, -70);
//        ofRotateZDeg(60-100*i);
//        ofDrawRectangle(0, -35, 20, 50);
//    ofPopMatrix();
//    //  right leg (upper/lower)
//    ofPushMatrix();
//        ofTranslate(10, -45);
//        ofRotateZDeg(30 + degRLeg);
//        ofDrawRectangle(0, -35, 20, 50);
//        ofTranslate(0, -70);
//        ofRotateZDeg(-60-i);
//        ofDrawRectangle(0, -35, 20, 50);
//    ofPopMatrix();
//    //  left arm (upper/lower)
//    ofPushMatrix();
//        ofTranslate(-35, 40);
//        ofRotateZDeg(-(30 + degLArm));
//        ofDrawRectangle(0, -30, 20, 45);
//        ofTranslate(0, -60);
//        ofRotateZDeg(-60+5*i);
//        ofDrawRectangle(0, -30, 20, 45);
//    ofPopMatrix();
//    //  right arm (upper/lower)
//    ofPushMatrix();
//        ofTranslate(35, 40);
//        ofRotateZDeg(30 + degRArm);
//        ofDrawRectangle(0, -30, 20, 45);
//        ofTranslate(0, -60);
//        ofRotateZDeg(60+10*i);
//        ofDrawRectangle(0, -30, 20, 45);
//    ofPopMatrix();
//
//    i++;
    
//    ofSetColor(125-125*sin(i), 125-125*sin(i), 125-125*sin(i));
//    ofDrawBitmapString("The Doll", 50, 50);
}

//--------------------------------------------------------------
void ofApp::keyPressed(int key){

}

//--------------------------------------------------------------
void ofApp::keyReleased(int key){

}

//--------------------------------------------------------------
void ofApp::mouseMoved(int x, int y ){

}

//--------------------------------------------------------------
void ofApp::mouseDragged(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mousePressed(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mouseReleased(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mouseEntered(int x, int y){

}

//--------------------------------------------------------------
void ofApp::mouseExited(int x, int y){

}

//--------------------------------------------------------------
void ofApp::windowResized(int w, int h){

}

//--------------------------------------------------------------
void ofApp::gotMessage(ofMessage msg){

}

//--------------------------------------------------------------
void ofApp::dragEvent(ofDragInfo dragInfo){ 

}
