import QtQuick 2.1
import QtQuick.Controls 2.4
import QtQuick.Window 2.2
import QtQuick.Controls.Material 2.3



ApplicationWindow {
	id: mainWindow
    title: "Kanji recognizer"

    minimumWidth : 350
    minimumHeight: 350

    Material.theme: Material.Dark

	width: 640
	height: 640

    visible: true

    property int menu_button_size: 30 

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

            source: "kanji_drawing_aid.png"
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

            icon.source: "clear.png"

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
            
            //ToDo: replace the BG image with an image for the canvas 
            width : drawing_aid.width > drawing_aid.height ? drawing_aid.height : drawing_aid.width
            height: drawing_aid.width > drawing_aid.height ? drawing_aid.height : drawing_aid.width

            x: mainWindow.width / 2 - width / 2
            y: mainWindow.height / 3 - height / 2

            property var color: "black"

            // all points which have been drawn
            // [[all points of Line_0], [all points of Line_1]]
            property var points: []
            //if the last stroke be removed
            property var undoLastStroke: false

            onPaint: {
                //setup path
                var ctx = getContext('2d')
                ctx.strokeStyle = "black"
                ctx.lineWidth = 2

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
                    python_canvas.get_current_image(canvas.toDataURL())
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
                    python_canvas.get_current_image(canvas.toDataURL())
                } 
            }
        }

        //predicted kanji selection
        Grid {
            id: "selection_grid"

            width:  5 * button_size + 4 * 10
            height: 2 * button_size + 2 * 10
            
            x: mainWindow.width / 2 - width / 2
            y: mainWindow.height - (height + button_size / 4)

            columns: 5
            rows: 2

            spacing: 10   

            property int button_size: 50


            CustomMaterialButton {
                id: "button_selection_0"

                text: ""
                font.pixelSize: selection_grid.button_size - 5
                
                width: selection_grid.button_size 
                height: selection_grid.button_size 

                onClicked: { text = predictionButton_0.button_pressed() }
            }
            CustomMaterialButton{
                text: ""
                font.pixelSize: selection_grid.button_size - 5
                
                width: selection_grid.button_size 
                height: selection_grid.button_size 

                onClicked: { text = predictionButton_1.button_pressed() }
            }
            CustomMaterialButton{
                text: ""
                font.pixelSize: selection_grid.button_size - 5
                
                width: selection_grid.button_size 
                height: selection_grid.button_size 

                onClicked: { text = predictionButton_2.button_pressed() }
            }
            CustomMaterialButton{
                text: ""
                font.pixelSize: selection_grid.button_size - 5
                
                width: selection_grid.button_size 
                height: selection_grid.button_size 

                onClicked: { text = predictionButton_3.button_pressed() }
            }
            CustomMaterialButton{
                text: ""
                font.pixelSize: selection_grid.button_size - 5
                
                width: selection_grid.button_size 
                height: selection_grid.button_size 

                onClicked: { text = predictionButton_4.button_pressed() }
            }
            CustomMaterialButton{
                text: ""
                font.pixelSize: selection_grid.button_size - 5
                
                width: selection_grid.button_size 
                height: selection_grid.button_size 

                onClicked: { text = predictionButton_5.button_pressed() }
            }
            CustomMaterialButton{
                text: ""
                font.pixelSize: selection_grid.button_size - 5
                
                width: selection_grid.button_size 
                height: selection_grid.button_size 

                onClicked: { text = predictionButton_6.button_pressed() }
            }
            CustomMaterialButton{
                text: ""
                font.pixelSize: selection_grid.button_size - 5
                
                width: selection_grid.button_size 
                height: selection_grid.button_size 

                onClicked: { text = predictionButton_7.button_pressed() }
            }
            CustomMaterialButton{
                text: ""
                font.pixelSize: selection_grid.button_size - 5
                
                width: selection_grid.button_size 
                height: selection_grid.button_size 

                onClicked: { text = predictionButton_8.button_pressed() }
            }
            CustomMaterialButton{
                text: ""
                font.pixelSize: selection_grid.button_size - 5
                
                width: selection_grid.button_size 
                height: selection_grid.button_size 

                onClicked: { text = predictionButton_9.button_pressed() }
            }
        }
    }
}