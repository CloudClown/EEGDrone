var keypress = require("keypress");
var arDrone = require('ar-drone');

//controls class
function DroneControls (controlMode) {
    this.client = arDrone.createClient();
    
    //configurations
    this.config = function() {
        this.client.config('general:navdata_demo', 'FALSE'); 
    };
    this.inspectNavigationData = function() {
        this.client.on('navdata', function(navdata) {
            if (navdata.demo) {
                console.log("Battery Left:"
                            +JSON.stringify(navdata.demo));
            }
        });
    };
    
    //flying dynamics
    this.yaw = function(isClockwise) {
        this.client.stop();
        if (isClockwise) {
            this.client.clockwise(0.2);
        } else {
            this.client.counterClockwise(0.2);
        }
    };
    this.pitch = function(isForward) {
        this.client.stop();
        if (isForward) {
            this.client.front(0.1);
        } else {
            this.client.back(0.1);
        }
    };
    this.roll = function(isLeft) {
        this.client.stop();
        if (isLeft) {
            this.client.left(0.1);
        } else {
            this.client.right(0.1);
        }
    };
    this.ascend = function(isUp) {
        this.client.stop();
        if (isUp) {
            this.client.up(0.2)
        } else {
            this.client.down(0.2);
        }
    };
    //initialization: execute configurations, inspect nav data, etc
    this.init = function () {
        console.log("Initializing Configurations...");
        this.config();
        console.log("Initializing Data Inspection...");
        this.inspectNavigationData();
    };
    
    //control modes
    //keyboard control
    this.keyBoardControl = function () {
        var dClient = this.client;
        var dControl = this;
        keypress(process.stdin);
        process.stdin.setRawMode(true);
        process.stdin.resume();
        process.stdin.on('keypress', function(ch, key) {
            console.log("input value: "+key.name);
            switch (key.name) {
            case 't': {
                console.log("taking off!");
                dClient.takeoff();
                break;
            }
            case 'l': {
                console.log("landing!");
                dClient.stop();
                dClient.land();
                break;
            }
            case 'q': {
                console.log("quiting!");
                dClient.stop();
                dClient.land();
                process.exit();
            }
            case 'a':{
                //roll left
                dControl.roll(true);
                console.log("rolling left!");
                break;
            }    
            case 'd':{
                //roll right
                dControl.roll(false);
                console.log("rolling right!");
                break;
            }
            case 'w':{
                //pitch front
                dControl.pitch(true);
                console.log("pitching front!");
                break;
            }
            case 's':{
                //pitch back
                dControl.pitch(false);
                console.log("pitching back!");
                break;
            }
            case 'u':{
                //ascend
                dControl.ascend(true);
                console.log("ascending!");
                break;
            }
            case 'j':{
                //descend
                dControl.ascend(false);
                console.log("descending!");
                break;
            }
            case 'h':{
                //yaw counter-clockwise
                dControl.yaw(false);
                console.log("yawing counter-clockwise!");
                break;
            }
            case 'k':{
                //yaw clock-wise
                dControl.yaw(true);
                console.log("yawing clockwise!");
                break;    
            }
            case 'space':{
                console.log("brake!");
                dClient.stop();
            }
            default:
                console.log("invalid command!");
                break;
            }
        });

    };
    //control by EEG epoc headset
    this.EEGControl = function () {

    };
    this.controlMode = controlMode;
    this.run = function() {
        if (this.controlMode === "keyboard") {
            this.keyBoardControl();
        } else if (this.controlMode == "eeg") {
            this.EEGControl();
        } else {
            console.log("Invalide Control Mode!");
            process.exit();
        }
    };
}

//start
var drone = new DroneControls("keyboard");
drone.init();
drone.run();
