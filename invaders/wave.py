"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the
Alien Invaders game.  Instances of Wave represent a single wave.  Whenever you
move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on screen.  
These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer.

# Elizabeth Healy (eah255)
# 12/3/17
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted 
# to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.
    
    This subcontroller has a reference to the ship, aliens, and any laser bolts on
    screen.It animates the laser bolts, removing any aliens as necessary. It also
    marches the aliens back and forth across the screen until they are all
    destroyed or they reach the defense line (at which point the player loses).
    When the wave is complete, you should create a NEW instance of Wave (in
    Invaders) if you want to make a new wave of aliens.
    
    If you want to pause the game, tell this controller to draw, but do not
    update.See subcontrollers.py from Lecture 24 for an example.
    This class will be similar to than one in how it interacts with the
    main class Invaders.
    
    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien
        or None] 
        _bolts:  the laser bolts currently on screen [list of Bolt, possibly
        empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number
        >= 0]
        
    
    As you can see, all of these attributes are hidden.  You may find that you
    want to access an attribute in class Invaders. It is okay if you do, but
    you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter and/or
    setter for any attribute that you need to access in Invaders.  Only add the
    getters and setters that you need for Invaders. You can keep everything else
    hidden.
    
    You may change any of the attributes above as you see fit. For example, may
    want to keep track of the score.  You also might want some label objects to
    display the score and number of lives. If you make changes, please list the
    changes with the invariants.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY:
    _alienDirection: keeps track of the direction the aliens are moving[string]
    _alienFire: The number of steps before the next bolt is fired by the aliens
    [int]
    _alienStep: the number of steps the aliens have taken since last bolt[int]
    _waveComplete: determines whether the wave is complete ie the aliens crossed
        the dline[1], all of the aliens are killed[2], or lives=0[3] [int]
    _alienSpeed : the number of seconds between alien steps
                [float 0.0<alienSpeed<=1.0]
    _soundOn: keeps track of whether the sound is on(True) or off(false)
                [boolean]
    _soundShip: sound that plays when ship fires bolt
                [Sound]
    _soundAlien: sound that plays when alien fires bolt
                [Sound]
    _soundAHit: sound that plays when alien is hit
                [Sound]
    _soundSHit: sound that plays when ship is hit
                [Sound]
        
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getShipType(self):
        """
        returns true is _ship is none and false otherwise
        """
        if(self._ship is None):
            return True
        else:
            return False
    def setShip(self, ship):
        """
        sets _ship to ship
        Parameter: ship is the ship to set _ship to
        Precondition: ship must be Ship()
        """
        assert isinstance(ship,Ship), 'ship is not Ship'
        self._ship=ship
        
    def getLives(self):
        """
        returns _lives, the number of lives the player has left
        """
        return self._lives
    
    def getWaveComplete(self):
        """
        returns _waveComplete
        """
        return self._waveComplete
    
    def getSoundOn(self):
        """ returns _soundOn"""
        return self._soundOn
    
    def getLives(self):
        """ returns numebr of lives"""
        return self._lives
        
    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self,speed,sound=True):
        """
        Initializer: creates a new wave of aliens (ALIEN_ROWS x ALIENS_IN_ROWS)
        First a 2d list of aliens is created that resembles what is to be drawn on
        the screen. (use helper function)
        Assigns various instance attributes to the correct values.
        
        Parameter: speed is the number of seconds between alien steps
        Precondition: 0<float<=1.0
        
        Parameter: sound determines if the sound for this wave starts on or off
        Precondition: sound is a bool
        """
        
        self._aliens=self._alienList()
        self._ship=Ship()
        self._bolts=[]
        self._dline=GPath(
            points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],
            linewidth=LINEWIDTH,linecolor=DLINE_COLOR)
        self._lives=SHIP_LIVES
        self._time=0
        self._alienDirection='right'
        self._alienFire=random.uniform(1,BOLT_RATE)
        self._alienStep=0
        self._waveComplete=0
        self._alienSpeed=speed
        self._soundOn=sound
        self._soundShip=Sound(SHIP_BOLT_SOUND)
        self._soundAlien=Sound(ALIEN_BOLT_SOUND)
        self._soundSHit=Sound(SHIP_HIT_SOUND)
        self._soundAHit=Sound(ALIEN_HIT_SOUND)
        
    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,dt,direction=''):
        """
        -keeps track of the time since the last alien movement
        -animates the ship, ship is moved left or right depending on the users
        input. Pressing the left arrow moves the ship to the left and pressing
        the right arrow moves the ship to the right
        -animates the aliens by calling the _moveAlien helper
        -animates the laser bolts
        
        Parameter: dt, the time in seconds since last update
        Precondition: dt is number (int or float)
        
        Parameter: direction is the direction of the arrow pressed
        Precondition: direction is a string
        """
        self._time=self._time+dt
        if(direction=='up'):
            if(self._isNotPlayerBolt() and type(self._ship)==Ship):    
                b=Bolt(self._ship.x,self._ship.y,'up')
                self._bolts.append(b)
                if(self._soundOn==True):
                        self._soundShip.play()
        if (direction=='left'):
            self._ship._moveShipLeft()
        if (direction=='right'):
            self._ship._moveShipRight()
        if(self._time>self._alienSpeed):
            self._moveAliens()
            self._time=0
        self._moveAndCheckBolts()
        self._checkBoltColAlien()
        self._checkBoltColShip()
        self._complete()
        
        
    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        """
        Draws the wave to the view.
        Uses the draw method from the GObject class
        
        Parameter: view is the the game view, used in drawing    
        Precondition: [instance of GView]
        """
        for row in self._aliens:
            for alien in row:
                if(type(alien)==Alien):
                    alien.draw(view)
        self._dline.draw(view)
        if(type(self._ship)==Ship):
            self._ship.draw(view)
        for bolt in self._bolts:
            bolt.draw(view)
            
            
    # HELPER METHODS FOR COLLISION DETECTION
    def _alienList(self):
        """
        creates a 2d alien list (ALIEN_ROWS x ALIENS_IN_ROWS)
        first row in list is row to be drawn at bottom
        
        Return: the 2d list of aliens created
        """
        alist=[]
        pickey=ALIEN_ROWS
        for r in range(ALIEN_ROWS):
            alist.append([])
            pickey=pickey-1
            for x in range(ALIENS_IN_ROW):
                #pic='alien'+str((pickey//2)%3+1)+'.png'
                pic=ALIEN_IMAGES[pickey//2%3]
                xpos=ALIEN_H_SEP*(x+1)+int(round(
                    ALIEN_WIDTH/2))+ALIEN_WIDTH*x
                ypos=GAME_HEIGHT-ALIEN_CEILING-ALIEN_V_SEP*r-(
                    ALIEN_HEIGHT)/2-ALIEN_HEIGHT*r
                a=Alien(xpos,ypos,pic)
                alist[r].append(a)
        return alist       
        
        
    def _moveAliens(self):
        """
        moves every alien ALIEN_H_WALK to the right or to the left. if the
        rightmost alien reaches the right edge, or if the leftmost alien
        reaches the left edge, the aliens move ALIEN_V_SEP down
        """
        if(self._alienDirection=='right'):
            if(GAME_WIDTH-self._getRightMostAlien().right<=ALIEN_H_SEP):
                for row in self._aliens:
                    for alien in row:
                        if(type(alien)==Alien):
                            alien.y=alien.y-ALIEN_V_SEP
                self._alienDirection='left'
            else:
                for row in self._aliens:
                    for alien in row:
                        if(type(alien)==Alien):
                            alien.x=alien.x+ALIEN_H_WALK
        elif(self._alienDirection=='left'):
            if(self._getLeftMostAlien().left<=ALIEN_H_SEP):
                for row in self._aliens:
                    for alien in row:
                        if(type(alien)==Alien):
                            alien.y=alien.y-ALIEN_V_SEP
                self._alienDirection='right'
            else:
                for row in self._aliens:
                    for alien in row:
                        if(type(alien)==Alien):
                            alien.x=alien.x-ALIEN_H_WALK
        self._alienStep=self._alienStep+1
        if(self._alienStep>=self._alienFire):
            self._alienStep=0
            self._fireAlienBolt()
            
            
    def _moveAndCheckBolts(self):
        """
        moves bolts and checks if they have gone off the top or bottom of
        the screen and needs to be deleted from _bolts
        """
        for bolt in self._bolts:
            bolt._moveBolt()
            if(bolt.bottom>=GAME_HEIGHT or bolt.top<=0):
                self._bolts.remove(bolt)
                
                
    def _isNotPlayerBolt(self):
        """
        checks every bolt in the list to determine if one of them is a
        player bolt
        RETURN: if there is a player bolt already in the list, the method
        returns false otherwise it returns True
        """
        for bolt in self._bolts:
            if bolt.getVel()>0:
                return False
        return True
    
    def _PlayerBolt(self):
        """
        checks every bolt in the list to determine if one of them is a
        player bolt
        RETURN: the player bolt or nothing if there are no player bolts
        """
        for bolt in self._bolts:
            if bolt.getVel()>0:
                return bolt
    
    def _fireAlienBolt(self):
        """
        if alienStep > alien fire, then a bolt is fired from a random column of
        aliens. the method ensures that there are aliens in the selected column
        """
        a=None
        while a==None:
            r=random.randrange(ALIENS_IN_ROW)
            
            for x in range(len(self._aliens)-1,-1,-1):
                if(isinstance(self._aliens[x][r],Alien) and a==None):
                    a=self._aliens[x][r]
                    b=Bolt(a.x,a.bottom-BOLT_HEIGHT/2,'down')
                    self._bolts.append(b)
                    if(self._soundOn==True):
                        self._soundAlien.play()
        self._alienFire=random.uniform(1,BOLT_RATE)
        
    def _checkBoltColAlien(self):
        """
        checks if the ship's bolt collides with an alien. if the bolt collides,
        the alien is removed from _aliens and replaced with NONE and the bolt is
        removed from _bolts
        """
        for row in self._aliens:
            for a in row:
                if type(
                    a)==Alien and not self._isNotPlayerBolt() and a.collides(
                    self._PlayerBolt()):
                    index=row.index(a)
                    row.remove(a)
                    row.insert(index, None)
                    for bolt in self._bolts:
                        if bolt.getVel()>0:
                            b=bolt
                    self._bolts.remove(b)
                    if(self._soundOn==True):
                        self._soundAHit.play()
    
    def _checkBoltColShip(self):
        """
        check if one of the aliens bolts collides with the ship
        if it collides, the ship is set to none and the bolt is removed
        from _bolts
        """
        for bolt in self._bolts:
            if bolt.getVel()<0 and self._ship is not None and self._ship.collides(
                bolt):
                self._ship=None
                self._bolts.remove(bolt)
                self._lives=self._lives-1
                if(self._soundOn==True):
                        self._soundSHit.play()
                
    def _complete(self):
        """
        changes waveComplete based on whether the aliens are below the dline,
        all aliens are killed, or lives =0
        """
        belowD=False
        killed=True
        for row in self._aliens:
            for alien in row:
                if isinstance(alien, Alien) and alien.bottom<DEFENSE_LINE:
                    belowD=True
                if isinstance(alien,Alien):
                    killed=False
        
        if self._lives==0:
            self._waveComplete=LIVES_LOST
        elif belowD==True:
            self._waveComplete=DLINE_CROSSED
        elif killed==True:
            self._waveComplete=ALIENS_KILLED
            
    def _getLeftMostAlien(self):
        """
        returns the left most alien that is not NONE
        """
        for col in range (ALIENS_IN_ROW):
            for row in range(ALIEN_ROWS):
                if(isinstance(self._aliens[row][col],Alien)):
                    a=self._aliens[row][col]
                    return a
                
    def _getRightMostAlien(self):
        """
        returns the right most alien that is not None
        """
        for col in range(ALIENS_IN_ROW-1,-1,-1):
            for row in range(ALIEN_ROWS):
                if(isinstance(self._aliens[row][col],Alien)):
                    a=self._aliens[row][col]
                    return a
                
    def switchSound(self):
        """
        turns the sound on or off, switches _soundOn from true to false or
        visa versa
        """
        if(self._soundOn==True):
            self._soundOn=False
        else:
            self._soundOn=True