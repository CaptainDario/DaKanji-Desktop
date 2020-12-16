import QtQuick 2.1
import QtQuick.Controls 2.4
import QtQuick.Window 2.2
import QtQuick.Controls.Material 2.3


ApplicationWindow {
	id: mainWindow

    title: "Kanji recognizer"

    Material.theme: Material.Dark

	width: 640
	height: 640

    visible: true

    Rectangle {

        width: mainWindow.width + 1
        height: mainWindow.height + 1
        color: "Grey" 

        //drawing aid BG image
        Image {
            id: "drawing_aid"
            objectName: "drawing_aid"

            x: parent.width / 2 - width / 2
            y: parent.height / 3 - height / 2

            width: parent.width / 100 * 50
            height: parent.height / 100 * 50

            anchors.centerIn: horizontalCenter

            source: "img/kanji_drawing_aid.png"
            sourceSize.height: 1024
            sourceSize.width: 1024
            fillMode: Image.PreserveAspectFit
        }

        //Canvas clear button
        Button{
            id: "button_clear"

            x: canvas.width + canvas.x - mainWindow.menu_button_size
            y: canvas.y - mainWindow.menu_button_size 

            width : mainWindow.menu_button_size
            height: mainWindow.menu_button_size

            padding: 10

            icon.source: "file:///E:/projects/kanji-recognizer/img/clear.png"

            onClicked: {
               canvas.points = new Array(0)
               canvas.getContext("2d").reset()
               canvas.requestPaint() 
            }
        }        
        //Undo last stroke button
        Button{
            id: "button_undo"

            x: canvas.width + canvas.x - 2*mainWindow.menu_button_size
            y: canvas.y - mainWindow.menu_button_size 

            width : mainWindow.menu_button_size
            height: mainWindow.menu_button_size

            padding: 10

            icon.source: "file:///E:/projects/kanji-recognizer/img/undo.png"

            onClicked: {
                canvas.undoLastStroke = true
                canvas.points.pop()
                canvas.getContext("2d").reset()
                canvas.requestPaint() 
            }
        }

        //Kanji drawing canvas
        Canvas {
            
            id: "canvas"
            
            width : drawing_aid.width > drawing_aid.height ? drawing_aid.height : drawing_aid.width
            height: drawing_aid.width > drawing_aid.height ? drawing_aid.height : drawing_aid.width

            x: mainWindow.width / 2 - width / 2
            y: mainWindow.height / 3 - height / 2

            property real lastX
            property real lastY

            onPaint: {
                var ctx = getContext('2d')
                ctx.lineWidth = 1.5
                ctx.strokeStyle = canvas.color
                ctx.beginPath()
                ctx.moveTo(lastX, lastY)
                lastX = area.mouseX
                lastY = area.mouseY
                ctx.lineTo(lastX, lastY)
                ctx.stroke()
            }

            MouseArea {
                id: area
                anchors.fill: parent

                onPressed: {
                    canvas.lastX = mouseX
                    canvas.lastY = mouseY
                }

                onPositionChanged: {
                    canvas.requestPaint()
                } 
            }
        }
}