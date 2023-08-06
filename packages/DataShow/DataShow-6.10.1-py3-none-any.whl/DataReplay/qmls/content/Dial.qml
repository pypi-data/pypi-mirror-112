import QtQuick 2.2

Item {
    id: root
    property real value : 0

    width: 210
    height: 210

    Image { source: "background.png" }

    Image {
        x: 96
        y: 35
        source: "needle_shadow.png"
        transform: Rotation {
            origin.x: 9
            origin.y: 67
            angle: needleRotation.angle
        }
    }

    Image {
        id: needle
        x: 98; y: 33
        antialiasing: true
        source: "needle.png"
        transform: Rotation {
            id: needleRotation
            origin.x: 5; 
            origin.y: 65
            angle: Math.min(Math.max(-130, root.value*2.6-130), 133)
            Behavior on angle {
                SpringAnimation {
                    spring: 1.4
                    damping: .15
                }
            }
        }
    }

    Image { x: 21; y: 18; source: "overlay.png" }
}
