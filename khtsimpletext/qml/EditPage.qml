import QtQuick 1.1
import com.nokia.meego 1.0
import 'components'
import 'common.js' as Common

Page {
    tools: editTools
    id: editPage

    property string filePath;
    property bool modified;

    signal refresh();
    
    onRefresh: {
               }
                            
    onFilePathChanged: {
        if (filePath !== '') {
            console.log('FilePathChanger');
            textEditor.text = QmlFileReaderWriter.read(filePath);
            modified = false;
            flick.returnToBounds();
            }
    }
    
    function exitFile() {    
        textEditor.text = '';
        filePath = '';
        modified = false;
        pageStack.pop();
    }

    function saveFile() {    
        QmlFileReaderWriter.write(filePath, textEditor.text);
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


    Flickable {
         id: flick
         flickableDirection: Flickable.VerticalFlick
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
         contentHeight: textEditor.height
         pressDelay: 200

             TextArea {
                 id: textEditor
                 height: Math.max (700, implicitHeight)
                 width: editPage.width + 4
                 wrapMode: TextEdit.Wrap
                 textFormat: TextEdit.PlainText
                 font { bold: false; family: "Nokia Pure Text"; pixelSize: 18;}
                 onTextChanged: { modified = true;}
         }
   
   
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


