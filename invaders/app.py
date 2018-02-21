"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders
application. There is no need for any additional classes in this module.
If you need more classes, 99% of the time they belong in either the wave
module or the models module. If you are unsure about where a new class
should go, post a question on Piazza.

# CITATION: function _wasSPressed was written with the help of
state.py by Walker White

# Elizabeth Healy (eah255)
# 12/3//17
"""
import cornell
from consts import *#GAME_WIDTH,GAME_HEIGHT,WELCOME_TEXT_SIZE
from game2d import *
from wave import *
import models



# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application
    
    This class extends GameApp and implements the various methods necessary
    for processing the player inputs and starting/running a game.
    
        Method start begins the application.
        
        Method update either changes the state or updates the Play object
        
        Method draw displays the Play object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.
    
    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.
    
    The primary purpose of this class is to manage the game state: which is when
    the game started, paused, completed, etc. It keeps track of that in an
    attribute called _state.
    
    INSTANCE ATTRIBUTES:
        view:   the game view, used in drawing (see examples from class)
                [instance of GView; it is inherited from GameApp]
        input:  the user input, used to control the ship and change state
                [instance of GInput; it is inherited from GameApp]
        _state: the current state of the game represented as a value from
                consts.py
                [one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED,
                STATE_CONTINUE, STATE_COMPLETE]
        _wave:  the subcontroller for a single wave, which manages the ships and
                aliens
                [Wave, or None if there is no wave currently active]
        _text:  the currently active message
                [GLabel, or None if there is no message to display]
        
    
    STATE SPECIFIC INVARIANTS: 
        Attribute _wave is only None if _state is STATE_INACTIVE.
        Attribute _text is only None if _state is STATE_ACTIVE.
    
    For a complete description of how the states work, see the specification
    for the method update.
    
    You may have more attributes if you wish (you might want an attribute to
    store any score across multiple waves). If you add new attributes, they
    need to be documented here.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    _lastkeys: the number of keys press in the last update
                [int>=0]
    _background: the background image
                [GImage]
    _numWins: the number of consecutive times the player has completed a wave
                successfully [int>=0]
    _soundLabel: the Glabel that gives inscructions on how to mute, attribute
                so it does not have to create a new label each time
                [GLabel]
    _soundStatus: keeps track of whether the sound is on or off so that it can
                    carry over to the next wave
                    [bool]
    _soundWin: sound that plays when player wins wave
                [Sound]
    _soundLose: sound that plays when player loses wave
                [Sound]
    """
    
    # DO NOT MAKE A NEW INITIALIZER!
    
    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.
        
        This method is distinct from the built-in initializer __init__ (which you 
        should not override or change). This method is called once the game is
        running. 
        You should use it to initialize any game specific attributes.
        
        This method should make sure that all of the attributes satisfy the given 
        invariants. When done, it sets the _state to STATE_INACTIVE and create a
        message (in attribute _text) saying that the user should press to play a
        game.
        """
        self._game=None
        self._soundWin=Sound(WIN_SOUND)
        self._soundLose=Sound(LOSE_SOUND)
        self._soundLabel=GLabel(text="Press 'M' to mute and 'U' to unmute")
        self._soundLabel.font_size=SOUND_TEXT_SIZE
        self._soundLabel.font_name=TEXT_FONT
        self._soundLabel.left=5
        self._soundLabel.bottom=5
        self._soundLabel.linecolor=TEXT_COLOR
        self._soundStatus=True
        self._numWins=0
        self._state=STATE_INACTIVE
        self._background=GImage(
            x=GAME_WIDTH/2,y=GAME_HEIGHT/2,
            width=GAME_WIDTH,height=GAME_HEIGHT, source=BACKGROUND)
        self._lastkeys=0
        self._wave=None
        if(self._state==STATE_INACTIVE):
            self._text=GLabel(text="Press 'S' to Play")
            self._text.font_size=WELCOME_TEXT_SIZE
            self._text.font_name= TEXT_FONT
            self._text.x=GAME_WIDTH//2
            self._text.y=GAME_HEIGHT//2
            self._text.linecolor=TEXT_COLOR
        else:
            self._text=None
        
    def update(self,dt):
        """
        Animates a single frame in the game.
        
        It is the method that does most of the work. It is NOT in charge of
        playing the game.  That is the purpose of the class Wave. The primary
        purpose of this game is to determine the current state, and -- if the game
        is active -- pass the input to the Wave object _wave to play the game.
        
        As part of the assignment, you are allowed to add your own states.
        However, at a minimum you must support the following states:
        STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE,
        and STATE_COMPLETE.  Each one of these  does its own thing and might even
        needs its own helper.  We describe these below.
        
        STATE_INACTIVE: This is the state when the application first opens.
        It is a paused state, waiting for the player to start the game.  It
        displays a simple message on the screen. The application remains in this
        state so long as the player never presses a key.  In addition, this is
        the state the application returns to when the game is over (all lives
        are lost or all aliens are dead).
        
        STATE_NEWWAVE: This is the state creates a new wave and shows it on the
        screen. The application switches to this state if the state was
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        This state only lasts one animation frame before switching to
        STATE_ACTIVE.
        
        STATE_ACTIVE: This is a session of normal gameplay.  The player can
        move theship and fire laser bolts.  All of this should be handled
        inside of class Wave (NOT in this class).  Hence the Wave class should
        have an update() method, just like the subcontroller example in lecture.
        
        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However,
        the game isstill visible on the screen.
        
        STATE_CONTINUE: This state restores the ship after it was destroyed. The 
        application switches to this state if the state was STATE_PAUSED in the 
        previous frame, and the player pressed a key. This state only lasts one
        animation  frame before switching to STATE_ACTIVE.
        
        STATE_COMPLETE: The wave is over, and is either won or lost.
        
        You are allowed to add more states if you wish. Should you do so, you
        should describe them here.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._wasSPressed()
        self._wasMPressed()
        self._wasUPressed()
        if (self._state==STATE_NEWWAVE): #change from new wave to active
            self._wave=Wave(ALIEN_SPEED*(3/4)**self._numWins,self._soundStatus)
            self._state=STATE_ACTIVE
        if(self._state==STATE_ACTIVE):
            self._checkDirectionKeyPress(dt)
        if(self._state==STATE_CONTINUE):
            self._state=STATE_ACTIVE
            self._text=None
            self._wave.setShip(Ship())
        self._determinieWinOrLose()
        self._wasEnterPressed()        
                
    def draw(self):
        """
        Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject.  To draw a
        GObject g, simply use the method g.draw(self.view).  It is that easy!
        
        Many of the GObjects (such as the ships, aliens, and bolts) are attributes
        in Wave. In order to draw them, you either need to add getters for these
        attributes or you need to add a draw method to class Wave.  We suggest
        the latter.  See the example subcontroller.py from class.
        """
        # IMPLEMENT ME
        self._background.draw(self.view)
        if (self._text!=None):
            self._text.draw(self.view)
        if(self._state==STATE_ACTIVE or self._state==STATE_PAUSED):
            self._wave.draw(self.view)
            self._soundLabel.draw(self.view)
        
    
    
    # HELPER METHODS FOR THE STATES GO HERE
    def _wasSPressed(self):
        """Determines if the state is inactive ie player is at welcome screen, or
        if the state is paused and if the s key, and only s key, was pressed to
        begin the game. Also updates _lastkeys to the current key_count
        
        """
        rightState=(self._state==STATE_INACTIVE)
        otherrightstate=(self._state==STATE_PAUSED)
        onlyOneKey=(self.input.key_count==1 and self._lastkeys==0)
        if  rightState and self.input.is_key_down('s')==True:
            # if s key and only s key pressed change state to STATE_NEWWAVE
            self._state=STATE_NEWWAVE
            self._text=None
        if otherrightstate:
            if self.input.key_count==1 and self.input.is_key_down('s')==True:
                self._state=STATE_CONTINUE
        self._lastkeys=self.input.key_count
      
    def _completeState(self,won=False):
        """
        changes _text to text for a completed game
        
        Parameter: won indicates whether the player won the game
        Precondition: bool
        """
        if(won==False):
            tex='the wave is over \n you lose \n press enter'
            if(self._soundStatus==True):
                self._soundLose.volume=1.0
                self._soundLose.play()
        else:
            tex='the wave is over \n you win \n press enter'
            if(self._soundStatus==True):
                self._soundWin.volume=1.0
                self._soundWin.play()
        self._text=GLabel(text=tex)
        self._text.font_size=PAUSED_TEXT_SIZE
        self._text.font_name= TEXT_FONT
        self._text.x=GAME_WIDTH//2
        self._text.y=GAME_HEIGHT//2
        self._text.linecolor=TEXT_COLOR
    
    
    def _pausedState(self):
        """
        changes _text for a paused game
        """
        self._text=GLabel(
                    text="you have "+str(
                        self._wave.getLives())+" lives left \n press 's' to play")
        self._text.font_size=PAUSED_TEXT_SIZE
        self._text.font_name= TEXT_FONT
        self._text.x=GAME_WIDTH/2
        self._text.y=GAME_HEIGHT/2
        self._text.linecolor=TEXT_COLOR
        
      
    def _wasEnterPressed(self):
        """
        determines if the state is completed and if the player presses the enter
        key and only the enter key.
        _lastkeys is updated to key_count
        """
        rightState=(self._state==STATE_COMPLETE)
        #otherrightstate=(self._state==STATE_PAUSED)
        onlyOneKey=(self.input.key_count==1)
        if  rightState and onlyOneKey and self.input.is_key_down('enter')==True:
            # if s key and only s key pressed change state to STATE_NEWWAVE
            self._state=STATE_INACTIVE
            self._text=GLabel(text="Press 'S' to Play")
            self._text.font_size=WELCOME_TEXT_SIZE
            self._text.font_name= TEXT_FONT
            self._text.x=GAME_WIDTH//2
            self._text.y=GAME_HEIGHT//2
            self._text.linecolor=TEXT_COLOR
            self._soundWin.volume=0.0
            self._soundLose.volume=0.0
        self._lastkeys=self.input.key_count
    
    def _checkDirectionKeyPress(self, dt):
        """
        checks to see if any of the directional keys were pressed and if they
        were,the wave is updated with respect to the key pressed, ie. feed
        the key pressed as a parameter of the update function for wave.
        Parameter: dt is the dt parameter from the update method - time in seconds
        since last update
        Precondition: dt is a number (float, int)
        """
        if self.input.is_key_down('left'):
            self._wave.update(dt,'left')
        elif self.input.is_key_down('right'):
            self._wave.update(dt,'right')
        elif self.input.is_key_down('up'):
            self._wave.update(dt,'up')
        else:
            self._wave.update(dt)
                
    def _wasMPressed(self):
        """
        determines if 'M' was pressed and if if was, switches the sound from on
        to off
        user can only switch sound during STATE_ACTIVE and STATE_PAUSED because
        that is the only time the label is drawn
        """
        rightState=(self._state==STATE_ACTIVE or self._state==STATE_PAUSED)
        unmuted=self._soundStatus==True
        if  rightState and unmuted and self.input.is_key_down('m')==True:
            self._wave.switchSound()
            self._soundStatus=False
        self._lastkeys=self.input.key_count
        
    def _wasUPressed(self):
        """
        determines if 'U' was pressed and if if was, switches the sound from off
        to on
        user can only switch sound during STATE_ACTIVE and STATE_PAUSED because
        that is the only time the label is drawn
        """
        rightState=(self._state==STATE_ACTIVE or self._state==STATE_PAUSED)
        muted=self._soundStatus==False
        if  rightState and muted and self.input.is_key_down('u')==True:
            self._wave.switchSound()
            self._soundStatus=True
        self._lastkeys=self.input.key_count
        
    def _determinieWinOrLose(self):
        """
        Determines if the game has been won or lost yet, determinies if all lives
        are lost, all aliens are destroyed, or if the aliens cross the dline
        
        If the game is lost or won, the state is changed to complete, _numWins is
        adjusted and _soundStatus is adjusted to the current sound status. Also
        the wave is deleted
        """
        if(self._wave is not None) and self._wave.getShipType():
            if(self._wave.getWaveComplete()==LIVES_LOST):
                self._state=STATE_COMPLETE
                self._completeState(False)
                self._numWins=0
                self._soundStatus=self._wave.getSoundOn()
                self._wave=None
            else:
                self._state=STATE_PAUSED
                self._pausedState()
        elif(self._wave is not None):
            if(self._wave.getWaveComplete()==ALIENS_KILLED):
                self._state=STATE_COMPLETE
                self._completeState(True)
                self._numWins+=1
                self._soundStatus=self._wave.getSoundOn()
                self._wave=None
            elif(self._wave.getWaveComplete()==DLINE_CROSSED):
                self._state=STATE_COMPLETE
                self._completeState(False)
                self._numWins+=1
                self._soundStatus=self._wave.getSoundOn()
                self._wave=None  
          
          
          
           