//
//  Doll.h
//  FinalAssignment
//
//  Created by Muyang Eric Huang on 2020/07/16.
//
#pragma once

#ifndef Doll_h
#define Doll_h

#include <stdio.h>
#include "ofMain.h"

class Doll{

public:
//private:  他のヒトにアクセスできないようにする．
    
    //  property, member. menbers or properties.
    float posX, posY, scaleXY;
    int colorR, colorG, colorB;
    float radius;
    float period, range;
    float LLeg, RLeg, LArm, RArm;
    float BodyM;
    float i;
    
    //  methods.
    void setup();
    void update();
    void draw();
    void setColor(int r, int g, int b);
    void setPosition(float x, float y);
    void setScale(float scale);
    void setPeriod(float msec);
    void setRange(float deg);
    
//    //  constructor.
//    dolls();
};

#endif /* Doll_h */
