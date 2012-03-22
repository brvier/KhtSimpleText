import QtQuick 1.1
import com.nokia.meego 1.0
//import '../common.js' as Common

Menu {
    id: itemMenu
    visualParent: pageStack

    //property PageStack pageStack
    property string filePath
    property string fileName
  
    MenuLayout {
        MenuItem {
            text: qsTr("Copy")
            enabled: false
            onClicked: ;
        }
        MenuItem {
            text: qsTr("Move")
            enabled: false
            onClicked: ;
        }
        MenuItem {
            text: qsTr("Rename")
            onClicked: pageStack.replace(renameFilePage, { filePath: filePath, fileName: fileName });
        }
        MenuItem {
            text: qsTr("Delete")
            onClicked: {
              deleteQueryDialog.filepath = filePath;
              deleteQueryDialog.open();
            }
        }
    }
}
