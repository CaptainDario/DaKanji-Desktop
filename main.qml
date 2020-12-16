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

}