import QtQuick 2.6
import QtQuick.Controls 2.4
import QtQuick.Window 2.2
import QtQuick.Controls.Material 2.3


ApplicationWindow {
	id: mainWindow
    title: "DaKanji - v" + qsTr(settings.version)

    minimumWidth : 350
    minimumHeight: 350

    Material.theme: settings.mode == 0 ? Material.Dark : Material.light

	width:  640 
	height: 640

    visible: true


    property int drawer_width: 320 

    // should the drawer be shown
    property bool inPortrait: true 

    // drawer label height
    property int drawer_item_height: 40
    
    // margin between items from drawer
    property int drawer_items_padding: 10

    // the size of the buttons of the canvas menu
    property int menu_button_size: 30


    // the drawer for the settings
    Drawer {
        id: drawer

        width: drawer_width
        height: mainWindow.height

        closePolicy: Popup.CloseOnPressOutside
        modal: inPortrait 
        interactive: inPortrait
        visible: !inPortrait

        // drawer background color
        Rectangle {
            anchors.fill: parent
            color: settings.mode == 0 ? "#2e2e2e" : "white"
        }

        // DaKanji banner
        Image {
            id: logo
            width: drawer_width / 2
            source: "../media/banner.png"
            fillMode: implicitWidth > width ? Image.PreserveAspectFit : Image.Pad
        }

        // textfield to enter a custom dictionary url
        TextField {
            id: url

            height: drawer_item_height
            width: drawer_width - 11
            x: 5
            y: logo.height + drawer_item_height
            
            placeholderText: qsTr("dictionary URL")
            text: qsTr(settings.dict)

            onTextEdited: {
                settings.dict = url.text
            }
        }

        // select dark / light mode combo box
        ComboBox{
            id: modes

            height: drawer_item_height
            width : drawer_width - 11
            x: 5
            y: logo.height + 2*drawer_item_height + drawer_items_padding

            model: ["dark mode", "light mode"]
            currentIndex: settings.mode

            background: Rectangle{
                color: "#FFFFFF"
            }

            onCurrentIndexChanged: {
                if(modes.currentIndex != settings.mode){
                    settings.mode = modes.currentIndex
                    canvas.undoLastStroke = true
                    canvas.getContext("2d").reset()
                    canvas.requestPaint()
                }
            }
        }
        
        //text and background of the "invert presses" option
        Rectangle{
            
            height: drawer_item_height
            width : drawer_width - 11
            x: 5
            y: logo.height + 3*drawer_item_height + 2*drawer_items_padding

            color: "#FFFFFF"
            
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    settings.invert_presses = !settings.invert_presses
                    invert_presses = settings.invert_presses
                    console.log(settings.invert_presses)
                } 
            }
        }
        Text{ 
            height: drawer_item_height
            width : drawer_width - 11
            x: 15
            y: logo.height + 3*drawer_item_height + 2*drawer_items_padding
            
            verticalAlignment: Text.AlignVCenter
            text: "Invert long/short press behavior"
            color: "black"
        }

        // the checkbox to invert the long / short presses
        CheckBox{
            id: invert_presses 

            x: drawer_width - width
            y: logo.height + 3*drawer_item_height + 2*drawer_items_padding

            checked: settings.invert_presses

            onToggled: {
                settings.invert_presses = !settings.invert_presses 
                console.log(settings.invert_presses)
            }
        }
        //text and background of the "how to use" label
        Rectangle{
            
            height: drawer_item_height
            width : drawer_width - 11
            x: 5
            y: mainWindow.height - (drawer_item_height + drawer_items_padding) 

            color: "#FFFFFF"
            
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    Qt.openUrlExternally("https://github.com/CaptainDario/DaKanji-Desktop#usage")
                } 
            }
        }
        Text{ 
            height: drawer_item_height
            width : drawer_width - 11
            x: 15
            y: mainWindow.height - (drawer_item_height + drawer_items_padding) 
            
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            text: "How to use this?"
            color: "black"
        }
    }

    Rectangle {

        width: mainWindow.width + 1
        height: mainWindow.height + 1
        color: settings.mode == 0 ? "#2e2e2e" : "white" 

        // open drawer button
        CustomMaterialButton{
            x: 5 
            y: 5

            width : mainWindow.menu_button_size
            height: mainWindow.menu_button_size

            Image {
                source: settings.mode == 0 ? "hamburger_w.png" : "hamburger_b.png"

                x: 3
                y: 3

                width: parent.width - x*2
                height: parent.height - y*2
            }

            onClicked:{
                drawer.visible = true
            }
        }    

        //drawing aid BG image
        Image {
            id: "drawing_aid"
            objectName: "drawing_aid"

            x: parent.width / 2 - width / 2
            y: parent.height / 3 - height / 2

            width: parent.width / 100 * 50
            height: parent.height / 100 * 50

            source: settings.mode == 0 ? "kanji_drawing_aid_w.png" : "kanji_drawing_aid_b.png"
            sourceSize.height: 1024
            sourceSize.width: 1024
            fillMode: Image.PreserveAspectFit
        }

        //Canvas clear button
        CustomMaterialButton{
            id: "button_clear"

            x: canvas.width + canvas.x - mainWindow.menu_button_size
            y: canvas.y - mainWindow.menu_button_size - 2

            width : mainWindow.menu_button_size
            height: mainWindow.menu_button_size

            padding: 0

            Image {
                source: settings.mode == 0 ? "clear_w.png" : "clear_b.png"

                x: 3
                y: 3

                width: parent.width - x*2
                height: parent.height - y*2
            }

            onClicked: {
               canvas.points = new Array(0)
               canvas.getContext("2d").reset()
               canvas.requestPaint() 
            }
        }
        //Undo last stroke button
        CustomMaterialButton{
            id: "button_undo"

            x: canvas.width + canvas.x - 2*mainWindow.menu_button_size - 5
            y: canvas.y - mainWindow.menu_button_size  - 2

            width : mainWindow.menu_button_size
            height: mainWindow.menu_button_size

            padding: 10

            Image {
                source: settings.mode == 0 ? "undo_w.png" : "undo_b.png"

                x: 3
                y: 3

                width: parent.width - x*2
                height: parent.height - y*2
            }

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
            
            //ToDo: replace the BG image with an image for the canvas 
            width : drawing_aid.width > drawing_aid.height ? drawing_aid.height : drawing_aid.width
            height: drawing_aid.width > drawing_aid.height ? drawing_aid.height : drawing_aid.width

            x: mainWindow.width / 2 - width / 2
            y: mainWindow.height / 3 - height / 2

            // all points which have been drawn
            // [[all points of Line_0], [all points of Line_1]]
            property var points: []
            //if the last stroke was removed
            property var undoLastStroke: false

            onPaint: {
                //setup path
                var ctx = getContext('2d')
                ctx.strokeStyle = settings.mode == 0 ? "white" : "black"
                ctx.lineWidth = 4

                //paint
                if(canvas.undoLastStroke === false && canvas.points.length > 0){
                    ctx.beginPath()
                    //move line start to last cursor pos
                    var length_lines  = canvas.points.length - 1
                    var length_points = canvas.points[length_lines].length - 1
                    ctx.moveTo(canvas.points[length_lines][length_points][0],
                                canvas.points[length_lines][length_points][1])
                    
                    //get new pos of pointer and draw line to there
                    canvas.points[length_lines].push([area.mouseX, area.mouseY])
                    ctx.lineTo(canvas.points[length_lines][length_points + 1][0],
                                canvas.points[length_lines][length_points + 1][1])
                    ctx.stroke()
                }
                //redraw everything from the "lines"-array
                else{
                    for(let line = 0; line < canvas.points.length; line++){
                        ctx.beginPath()
                        for(let point = 0; point < canvas.points[line].length - 1; point++){
                            
                            ctx.moveTo(canvas.points[line][point][0],
                                        canvas.points[line][point][1])
                            
                            //get new pos of pointer and draw line to there
                            ctx.lineTo(canvas.points[line][point + 1][0],
                                        canvas.points[line][point + 1][1])

                        }
                        ctx.stroke()
                    }
                    canvas.undoLastStroke = false
                    //send the new image to python
                    ui.predict_from_image(canvas.toDataURL())
                }
            }

            MouseArea {
                id: area
                anchors.fill: parent

                onPressed: {
                    canvas.points.push([ [mouseX, mouseY] ])
                }

                onPositionChanged: {
                    canvas.requestPaint()
                }
                onReleased: {
                    ui.predict_from_image(canvas.toDataURL())
                } 
            }
        }

        //predicted kanji selection
        Grid {
            id: "selection_grid"

            x: mainWindow.width / 2 - width / 2
            y: mainWindow.height - (height + button_size / 4)

            columns: 5
            rows: 2

            spacing: 10   

            property int button_size: 50

            // the buttons from which the user can copy the predictions
            CustomMaterialButton {
                text: prediction_button_1.character
                font.pixelSize: selection_grid.button_size - 5

                width: selection_grid.button_size 
                height: selection_grid.button_size 

                function press() {
                    prediction_button_1.button_pressed()

                    if(prediction_button_1.character != ""){
                        popup_1.open()
                        popup_1_timer.start()
                    }
                }
                function long_press() {
                    prediction_button_1.button_long_pressed(settings.dict)
                }

                onClicked: {
                    if(!settings.invert_presses)
                        press()
                    else
                        long_press()
                }
                onPressAndHold: {
                    if(!settings.invert_presses)
                        long_press()
                    else
                        press()
                }
                Popup {
                    id: popup_1

                    parent: Overlay.overlay

                    x: 0 
                    y: mainWindow.height - height
                    width: mainWindow.width
                    height: 50
                    contentWidth: mainWindow.width

                    contentItem: Text {
                        text: "Copied " + prediction_button_1.character + " to clipboard"
                        verticalAlignment: Text.AlignVCenter
                    }
                    enter: Transition {
                        NumberAnimation { 
                            property: "y"; from: 640; to: 590
                        }
                    }
                    exit: Transition {
                        NumberAnimation { 
                            property: "y"; from: 590; to: 640
                        }
                    }
                }
                Timer{
                    id: popup_1_timer
                    interval: 1000
                    onTriggered: popup_1.close()
                }
            }
            CustomMaterialButton{
                text: prediction_button_2.character
                font.pixelSize: selection_grid.button_size - 5
                
                width: selection_grid.button_size 
                height: selection_grid.button_size 

                function press() {
                    prediction_button_2.button_pressed()

                    if(prediction_button_2.character != ""){
                        popup_2.open()
                        popup_2_timer.start()
                    }
                }
                function long_press() {
                    prediction_button_2.button_long_pressed(settings.dict)
                }

                onClicked: {
                    if(!settings.invert_presses)
                        press()
                    else
                        long_press()
                }
                onPressAndHold: {
                    if(!settings.invert_presses)
                        long_press()
                    else
                        press()
                }

                Popup {
                    id: popup_2

                    parent: Overlay.overlay

                    x: 0 
                    y: mainWindow.height - height
                    width: mainWindow.width
                    height: 50
                    contentWidth: mainWindow.width

                    contentItem: Text {
                        text: "Copied " + prediction_button_2.character + " to clipboard"
                    }
                    enter: Transition {
                        NumberAnimation { 
                            property: "y"; from: 640; to: 590
                        }
                    }
                    exit: Transition {
                        NumberAnimation { 
                            property: "y"; from: 590; to: 640
                        }
                    }
                }
                Timer{
                    id: popup_2_timer
                    interval: 1000
                    onTriggered: popup_2.close()
                }
            }
            CustomMaterialButton{
                text: prediction_button_3.character
                font.pixelSize: selection_grid.button_size - 5
                
                width: selection_grid.button_size 
                height: selection_grid.button_size 

                function press() {
                    prediction_button_3.button_pressed()

                    if(prediction_button_3.character != ""){
                        popup_3.open()
                        popup_3_timer.start()
                    }
                }
                function long_press() {
                    prediction_button_3.button_long_pressed(settings.dict)
                }

                onClicked: {
                    if(!settings.invert_presses)
                        press()
                    else
                        long_press()
                }
                onPressAndHold: {
                    if(!settings.invert_presses)
                        long_press()
                    else
                        press()
                }

                Popup {
                    id: popup_3

                    parent: Overlay.overlay

                    x: 0 
                    y: mainWindow.height - height
                    width: mainWindow.width
                    height: 50
                    contentWidth: mainWindow.width

                    contentItem: Text {
                        text: "Copied " + prediction_button_3.character + " to clipboard"
                    }
                    enter: Transition {
                        NumberAnimation { 
                            property: "y"; from: 640; to: 590
                        }
                    }
                    exit: Transition {
                        NumberAnimation { 
                            property: "y"; from: 590; to: 640
                        }
                    }
                }
                Timer{
                    id: popup_3_timer
                    interval: 1000
                    onTriggered: popup_3.close()
                }
            }
            CustomMaterialButton{
                text: prediction_button_4.character
                font.pixelSize: selection_grid.button_size - 5
                
                width: selection_grid.button_size 
                height: selection_grid.button_size 

                function press() {
                    prediction_button_4.button_pressed()

                    if(prediction_button_4.character != ""){
                        popup_4.open()
                        popup_4_timer.start()
                    }
                }
                function long_press() {
                    prediction_button_4.button_long_pressed(settings.dict)
                }

                onClicked: {
                    if(!settings.invert_presses)
                        press()
                    else
                        long_press()
                }
                onPressAndHold: {
                    if(!settings.invert_presses)
                        long_press()
                    else
                        press()
                }

                Popup {
                    id: popup_4

                    parent: Overlay.overlay

                    x: 0 
                    y: mainWindow.height - height
                    width: mainWindow.width
                    height: 50
                    contentWidth: mainWindow.width

                    contentItem: Text {
                        text: "Copied " + prediction_button_4.character + " to clipboard"
                    }
                    enter: Transition {
                        NumberAnimation { 
                            property: "y"; from: 640; to: 590
                        }
                    }
                    exit: Transition {
                        NumberAnimation { 
                            property: "y"; from: 590; to: 640
                        }
                    }
                }
                Timer{
                    id: popup_4_timer
                    interval: 1000
                    onTriggered: popup_4.close()
                }
            }
            CustomMaterialButton{
                text: prediction_button_5.character
                font.pixelSize: selection_grid.button_size - 5
                
                width: selection_grid.button_size 
                height: selection_grid.button_size 

                function press() {
                    prediction_button_5.button_pressed()

                    if(prediction_button_5.character != ""){
                        popup_5.open()
                        popup_5_timer.start()
                    }
                }
                function long_press() {
                    prediction_button_5.button_long_pressed(settings.dict)
                }

                onClicked: {
                    if(!settings.invert_presses)
                        press()
                    else
                        long_press()
                }
                onPressAndHold: {
                    if(!settings.invert_presses)
                        long_press()
                    else
                        press()
                }

                Popup {
                    id: popup_5

                    parent: Overlay.overlay

                    x: 0 
                    y: mainWindow.height - height
                    width: mainWindow.width
                    height: 50
                    contentWidth: mainWindow.width

                    contentItem: Text {
                        text: "Copied " + prediction_button_5.character + " to clipboard"
                    }
                    enter: Transition {
                        NumberAnimation { 
                            property: "y"; from: 640; to: 590
                        }
                    }
                    exit: Transition {
                        NumberAnimation { 
                            property: "y"; from: 590; to: 640
                        }
                    }
                }
                Timer{
                    id: popup_5_timer
                    interval: 1000
                    onTriggered: popup_5.close()
                }
            }
            CustomMaterialButton{
                text: prediction_button_6.character
                font.pixelSize: selection_grid.button_size - 5
                
                width: selection_grid.button_size 
                height: selection_grid.button_size 

                function press() {
                    prediction_button_6.button_pressed()

                    if(prediction_button_6.character != ""){
                        popup_6.open()
                        popup_6_timer.start()
                    }
                }
                function long_press() {
                    prediction_button_6.button_long_pressed(settings.dict)
                }

                onClicked: {
                    if(!settings.invert_presses)
                        press()
                    else
                        long_press()
                }
                onPressAndHold: {
                    if(!settings.invert_presses)
                        long_press()
                    else
                        press()
                }

                Popup {
                    id: popup_6

                    parent: Overlay.overlay

                    x: 0 
                    y: mainWindow.height - height
                    width: mainWindow.width
                    height: 50
                    contentWidth: mainWindow.width

                    contentItem: Text {
                        text: "Copied " + prediction_button_6.character + " to clipboard"
                    }
                    enter: Transition {
                        NumberAnimation { 
                            property: "y"; from: 640; to: 590
                        }
                    }
                    exit: Transition {
                        NumberAnimation { 
                            property: "y"; from: 590; to: 640
                        }
                    }
                }
                Timer{
                    id: popup_6_timer
                    interval: 1000
                    onTriggered: popup_6.close()
                }
            }
            CustomMaterialButton{
                text: prediction_button_7.character
                font.pixelSize: selection_grid.button_size - 5
                
                width: selection_grid.button_size 
                height: selection_grid.button_size 

                function press() {
                    prediction_button_7.button_pressed()

                    if(prediction_button_7.character != ""){
                        popup_7.open()
                        popup_7_timer.start()
                    }
                }
                function long_press() {
                    prediction_button_7.button_long_pressed(settings.dict)
                }

                onClicked: {
                    if(!settings.invert_presses)
                        press()
                    else
                        long_press()
                }
                onPressAndHold: {
                    if(!settings.invert_presses)
                        long_press()
                    else
                        press()
                }

                Popup {
                    id: popup_7

                    parent: Overlay.overlay

                    x: 0 
                    y: mainWindow.height - height
                    width: mainWindow.width
                    height: 50
                    contentWidth: mainWindow.width

                    contentItem: Text {
                        text: "Copied " + prediction_button_7.character + " to clipboard"
                    }
                    enter: Transition {
                        NumberAnimation { 
                            property: "y"; from: 640; to: 590
                        }
                    }
                    exit: Transition {
                        NumberAnimation { 
                            property: "y"; from: 590; to: 640
                        }
                    }
                }
                Timer{
                    id: popup_7_timer
                    interval: 1000
                    onTriggered: popup_7.close()
                }
            }
            CustomMaterialButton{
                text: prediction_button_8.character
                font.pixelSize: selection_grid.button_size - 5
                
                width: selection_grid.button_size 
                height: selection_grid.button_size 

                function press() {
                    prediction_button_8.button_pressed()

                    if(prediction_button_8.character != ""){
                        popup_8.open()
                        popup_8_timer.start()
                    }
                }
                function long_press() {
                    prediction_button_8.button_long_pressed(settings.dict)
                }

                onClicked: {
                    if(!settings.invert_presses)
                        press()
                    else
                        long_press()
                }
                onPressAndHold: {
                    if(!settings.invert_presses)
                        long_press()
                    else
                        press()
                }

                Popup {
                    id: popup_8

                    parent: Overlay.overlay

                    x: 0 
                    y: mainWindow.height - height
                    width: mainWindow.width
                    height: 50
                    contentWidth: mainWindow.width

                    contentItem: Text {
                        text: "Copied " + prediction_button_8.character + " to clipboard"
                    }
                    enter: Transition {
                        NumberAnimation { 
                            property: "y"; from: 640; to: 590
                        }
                    }
                    exit: Transition {
                        NumberAnimation { 
                            property: "y"; from: 590; to: 640
                        }
                    }
                }
                Timer{
                    id: popup_8_timer
                    interval: 1000
                    onTriggered: popup_8.close()
                }
            }
            CustomMaterialButton{
                text: prediction_button_9.character
                font.pixelSize: selection_grid.button_size - 5
                
                width: selection_grid.button_size 
                height: selection_grid.button_size 

                function press() {
                    prediction_button_9.button_pressed()

                    if(prediction_button_9.character != ""){
                        popup_9.open()
                        popup_9_timer.start()
                    }
                }
                function long_press() {
                    prediction_button_9.button_long_pressed(settings.dict)
                }

                onClicked: {
                    if(!settings.invert_presses)
                        press()
                    else
                        long_press()
                }
                onPressAndHold: {
                    if(!settings.invert_presses)
                        long_press()
                    else
                        press()
                }

                Popup {
                    id: popup_9

                    parent: Overlay.overlay

                    x: 0 
                    y: mainWindow.height - height
                    width: mainWindow.width
                    height: 50
                    contentWidth: mainWindow.width

                    contentItem: Text {
                        text: "Copied " + prediction_button_9.character + " to clipboard"
                    }
                    enter: Transition {
                        NumberAnimation { 
                            property: "y"; from: 640; to: 590
                        }
                    }
                    exit: Transition {
                        NumberAnimation { 
                            property: "y"; from: 590; to: 640
                        }
                    }
                }
                Timer{
                    id: popup_9_timer
                    interval: 1000
                    onTriggered: popup_9.close()
                }
            }
            CustomMaterialButton{
                text: prediction_button_10.character
                font.pixelSize: selection_grid.button_size - 5
                
                width: selection_grid.button_size 
                height: selection_grid.button_size 

                function press() {
                    prediction_button_10.button_pressed()

                    if(prediction_button_10.character != ""){
                        popup_10.open()
                        popup_10_timer.start()
                    }
                }
                function long_press() {
                    prediction_button_10.button_long_pressed(settings.dict)
                }

                onClicked: {
                    if(!settings.invert_presses)
                        press()
                    else
                        long_press()
                }
                onPressAndHold: {
                    if(!settings.invert_presses)
                        long_press()
                    else
                        press()
                }

                Popup {
                    id: popup_10

                    parent: Overlay.overlay

                    x: 0 
                    y: mainWindow.height - height
                    width: mainWindow.width
                    height: 50
                    contentWidth: mainWindow.width

                    contentItem: Text {
                        text: "Copied " + prediction_button_10.character + " to clipboard"
                    }
                    enter: Transition {
                        NumberAnimation { 
                            property: "y"; from: 640; to: 590
                        }
                    }
                    exit: Transition {
                        NumberAnimation { 
                            property: "y"; from: 590; to: 640
                        }
                    }
                }
                Timer{
                    id: popup_10_timer
                    interval: 1000
                    onTriggered: popup_10.close()
                }
            }
        }
    }
}