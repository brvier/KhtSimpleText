import QtQuick 1.1
import com.nokia.meego 1.0

Page {
    tools: editTools

    property string filePath;
    property bool modified;

    onFilePathChanged: {
        if (filePath !== '') {
            console.log('FilePathChanger');
            textEditor.text = QmlFileReaderWriter.read(filePath);
            modified = false;
            }
    }

    //Component.onDestruction: {console.log('onDestruction');if (modified == true ) unsavedDialog.open(); }
    
    function exitFile() {    
        textEditor.text = '';
        filePath = '';
        modified = false;
        pageStack.pop();
    }

    function saveFile() {    
        QmlFileReaderWriter.write(filePath, textEditor.text);
    }
        
    QueryDialog {
	            id:unsavedDialog
                titleText:"Unsaved"
                icon: Qt.resolvedUrl('../icons/khtsimpletext.png')
                message:"Did you want to save file before closing it ?";
                acceptButtonText: 'Save';
                rejectButtonText: 'Cancel';
                onRejected: { exitFile(); }
                onAccepted: { saveFile();exitFile(); }
                }

    Rectangle {
        id:header
        anchors.top: parent.top
        width:parent.width
        height:70
        color:'darkgrey'
        z:2

        Text{
            id:headerlabel
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.left: parent.left
            anchors.topMargin: 5
            anchors.leftMargin: 10
            anchors.rightMargin: 50
            font { bold: false; family: "Nokia Pure Text"; pixelSize: 30; }
            color:"white"
            text:'KhtSimpleText'
        }
 
        Text{
            id:headerpathlabel
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            anchors.left: parent.left
            anchors.bottomMargin: 5
            anchors.leftMargin: 10
            anchors.rightMargin: 50
            font { bold: false; family: "Nokia Pure Text"; pixelSize: 16; }
            color:"#cc6633"
            text:filePath
        }
        
        /*Image{
            anchors.right: parent.right
            anchors.rightMargin: 10
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.topMargin: 10
            anchors.bottomMargin: 10
            //opacity: textEditor.activeFocus ? 1.0 : 0.5
            source:"image://theme/icon-m-framework-close-thumbnail"
            MouseArea{
                //id:closeVKBArea
                anchors.fill: parent
                //onClicked: textEditor.closeSoftwareInputPanel();
                onClicked: { 
                    if (!textEditor.focus) { 
                        textEditor.forceActiveFocus();
                        textEditor.openSoftwareInputPanel(); } 
                    else { 
                         textEditor.focus = false; 
                         textEditor.closeSoftwareInputPanel();}
                }
            }
        }*/
   }


    Flickable {
         id: flick
         flickableDirection: Flickable.VerticalFlick
         anchors.top: header.bottom
         anchors.left: parent.left
         anchors.leftMargin: 2
         anchors.right: parent.right
         anchors.rightMargin: 2
         anchors.bottom: parent.bottom
         anchors.bottomMargin: 2
         
         contentWidth: textEditor.width
         contentHeight: textEditor.height
         pressDelay: 100

             TextArea {
                 id: textEditor
                 anchors {left: parent.left; right: parent.right;}
                 height: Math.max (700, implicitHeight)
                 width: flick.width
	                 wrapMode: TextEdit.Wrap
                 font { bold: false; family: "Nokia Pure Text"; pixelSize: 18;}
                 onTextChanged: { modified = true; console.log('onTextChanged');}
         }
   
   
     }
    
    ToolBarLayout {
        id: editTools
        visible: true
        ToolIcon {
            platformIconId: "toolbar-back"
            anchors.left: (parent === undefined) ? undefined : parent.left
            onClicked: {
                   //console.log('onClicked (Back toolButton)');
                   if (modified == true ) unsavedDialog.open(); 
                   else exitFile();
                   }
        }
        /*ToolIcon {
                    platformIconId: "toolbar-save"
                                anchors.left: (parent === undefined) ? undefined : parent.left
                                            onClicked: pageStack.pop();
          }*/
        ToolIcon {
            platformIconId: "toolbar-view-menu"
            anchors.right: (parent === undefined) ? undefined : parent.right
            onClicked: (myMenu.status === DialogStatus.Closed) ? myMenu.open() : myMenu.close()
        }
    }
    
    
    
}


