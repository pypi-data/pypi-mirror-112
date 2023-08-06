import QtQuick 2.2
import QtQuick.Window 2.1
import QtQuick.Controls 1.4
import "content"


Rectangle{
    color: "#545454"
    width: 420
    height: 220

    function update_speed(speed){
        // don't change 1.2 because it's calcuated by data interpolation.
        dial.value = speed/1.2
    }

    function update_acc(acc_status){
        if (acc_status==0) {
            acc.color = "red"
        }
        else{
            acc.color="white"
        }
    }

    function update_enable(en_status){
        if(en_status==0){
            enable_ff.color = "red"
        }
        else{
            enable_ff.color = "white"
        }
    }

    function update_left_indi(left_indicator_status){
        if (left_indicator_status==0) {
            left_indicator.color = "yellow"
        }
        else{
            left_indicator.color="white"
        }
    }

    function update_right_indi(right_indicator_status){
        if (right_indicator_status==0) {
            right_indicator.color = "yellow"
        }
        else{
            right_indicator.color="white"
        }
    }

    Dial {
        id: dial
        anchors.left: parent.left
        anchors.leftMargin: 10
        anchors.top: parent.top
        anchors.topMargin:10
        value: 0
    }

    Rectangle{
        id: acc
        x:220
        y:20
        width: 80
        height: 30
        color: "white"
        radius:12
        Text {
            text: "ACC"
            color: "black"
            font.pixelSize: 20
            font.bold: true
            anchors.centerIn: parent
        }
    }

    Rectangle{
        id: enable_ff
        x: 320
        y: 20
        width: 80
        height: 30
        color: "white"
        radius: 12
        Text {
            text: "Enable"
            color: "black"
            font.pixelSize: 20
            font.bold: true
            anchors.centerIn: parent
        }
    }

    Rectangle{
        id: left_indicator
        x:220
        y:60
        width: 80
        height: 30
        color: "white"
        radius:12
        Text {
            text: "L-Steer"
            color: "black"
            font.pixelSize: 20
            font.bold: true
            anchors.centerIn: parent
        }
    }

    Rectangle{
        id: right_indicator
        x: 320
        y: 60
        width: 80
        height: 30
        color: "white"
        radius: 12
        Text {
            text: "R-Steer"
            color: "black"
            font.pixelSize: 20
            font.bold: true
            anchors.centerIn: parent
        }
    }

    Rectangle{
        id: line_split
        x:220
        y:110
        width:180
        height:5
        gradient: Gradient{
            GradientStop{
                position: 0.0
                color: "white"
            }
            GradientStop{
                position: 1.0
                color: "black"
            }
        }
    }

    Rectangle{
        id: ff_mode
        x:220
        y:130
        width: 180
        height: 30
        color: "white"
        radius:12
        Text {
            text: "BSD"
            color: "black"
            font.pixelSize: 20
            font.bold: true
            anchors.centerIn: parent
        }
    }

    Rectangle{
        id: left_warn
        x:220
        y:170
        width: 80
        height: 30
        color: "white"
        radius:12
        Text {
            text: "L-Warn"
            color: "black"
            font.pixelSize: 20
            font.bold: true
            anchors.centerIn: parent
        }
    }

    Rectangle{
        id: right_warn
        x: 320
        y: 170
        width: 80
        height: 30
        color: "white"
        radius: 12
        Text {
            text: "R-Warn"
            color: "black"
            font.pixelSize: 20
            font.bold: true
            anchors.centerIn: parent
        }
    }
}