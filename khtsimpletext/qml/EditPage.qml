import QtQuick 1.1
import com.nokia.meego 1.0
import 'components'
import 'common.js' as Common

Page {
    tools: editTools
    id: editPage

    property string filePath;
    property bool modified;
    property bool colored;

    signal refresh();

    onRefresh: {
               }

    onFilePathChanged: {
        if (filePath !== '') {
            console.log('FilePathChanger');
            Document.load(filePath)
            modified = false;
            flick.returnToBounds();
            console.log('End filepathchanger');
            }
    }

    function exitFile() {
        modified = false;
        pageStack.pop();
    }

    function saveFile() {
        Document.write(textEditor.text);
        modified = false;
    }

    QueryDialog {
                id:unsavedDialog
                titleText:"Unsaved"
                icon: Qt.resolvedUrl('../icons/khtsimpletext.png')
                message:"Did you want to save file before closing it ?";
                acceptButtonText: 'Save';
                rejectButtonText: 'Close';
                onRejected: { exitFile(); }
                onAccepted: { saveFile();exitFile(); }
                }

        PageHeader {
         id: header
         title: 'KhtSimpleText'
         subtitle: Common.beautifulPath(filePath);
    }

     BusyIndicator {
        id: busyindicator
        platformStyle: BusyIndicatorStyle { size: "large" }
        running: Document.ready ? false : true;
        opacity: Document.ready ? 0.0 : 1.0;
        anchors.centerIn: parent
    }

    Flickable {
         id: flick
         opacity: Document.ready ? 1.0 : 0.0
         flickableDirection: Flickable.HorizontalAndVerticalFlick
         //boundsBehavior: Flickable.DragOverBounds
         anchors.top: header.bottom
         anchors.left: parent.left
         anchors.leftMargin: -2
         anchors.right: parent.right
         anchors.rightMargin: -2
         anchors.bottom: parent.bottom
         anchors.bottomMargin: -2
         anchors.topMargin: -2
         clip: true

         contentWidth: textEditor.width
         contentHeight: textEditor.implicitHeight
         pressDelay: 200


             TextArea {
                 id: textEditor
                 anchors.top: parent.top
                 text: Document.text
                 height: Math.max (flick.height, implicitHeight)
                 width: (wrapMode == TextEdit.NoWrap) ? Math.max(flick.width +4,  textFalseEditor.paintedWidth + 28) : flick.width + 4
                 wrapMode: Document.colored ? TextEdit.NoWrap : (Settings.textWrap ? TextEdit.WordWrap : TextEdit.NoWrap);
                 inputMethodHints: Document.colored ? Qt.ImhNoAutoUppercase | Qt.ImhNoPredictiveText : Qt.ImhAutoUppercase | Qt.ImhPredictiveText;
                 textFormat: TextEdit.AutoText
                 font { bold: false; family: Settings.fontFamily; pixelSize: Settings.fontSize;}
                 onTextChanged: { modified = true; }
                 //onWidthChanged: {  console.log('WithChanged');}

         }
         
         onOpacityChanged: {
           if (flick.opacity == 1.0) modified = false;
         }
     }

         TextEdit {
             id:textFalseEditor
             text: Document.text
             font: textEditor.font
             textFormat: textEditor.textFormat
             wrapMode: textEditor.wrapMode
             opacity: 0.0
             }

    ScrollDecorator {
        flickableItem: flick
        platformStyle: ScrollDecoratorStyle {
        }}

    Menu {
        id: editMenu
        visualParent: pageStack
        MenuLayout {
            MenuItem { text: qsTr("About"); onClicked: about.open()}
            MenuItem { text: qsTr("MarkDown Preview"); onClicked: pageStack.push(previewPage, {atext:textEditor.text}); }
            MenuItem { text: qsTr("ReHighlight Text"); onClicked:{ Document.recolorIt(textEditor.text);} }
            MenuItem { text: qsTr("Save"); onClicked: saveFile()}
            /*MenuItem { text: qsTr("Preferences"); onClicked: notYetAvailableBanner.show(); }*/
        }
    }

    ToolBarLayout {
        id: editTools
        visible: true
        ToolIcon {
            platformIconId: "toolbar-back"
            anchors.left: (parent === undefined) ? undefined : parent.left
            onClicked: {
                   if (modified == true ) unsavedDialog.open();
                   else exitFile();
                   }
        }

        ToolIcon {
            platformIconId: "toolbar-view-menu"
            anchors.right: (parent === undefined) ? undefined : parent.right
            onClicked: (editMenu.status === DialogStatus.Closed) ? editMenu.open() : editMenu.close()
        }
    }
}


