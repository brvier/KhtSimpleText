import QtQuick 1.1
import com.nokia.meego 1.0
//import '../common.js' as Common

Menu {
    id: itemMenu
    visualParent: pageStack

    property string filePath
    property string fileName
    property int index

    MenuLayout {
        MenuItem {
            text: qsTr("Copy")
            onClicked: {
                var copyFilePage = Qt.createComponent(Qt.resolvedUrl("../CopyFilePage.qml"));
                pageStack.push(copyFilePage, { filePath: filePath, fileName: fileName, index: index });
            }
        }
        MenuItem {
            text: qsTr("Move")
            onClicked: {
                var moveFilePage = Qt.createComponent(Qt.resolvedUrl("../MoveFilePage.qml"));
                pageStack.push(moveFilePage, { filePath: filePath, fileName: fileName, index: index });
            }
        }
        MenuItem {
            text: qsTr("Rename")
            onClicked: {
                var renameFilePage = Qt.createComponent(Qt.resolvedUrl("../RenamePage.qml"));
                pageStack.push(renameFilePage, { filePath: filePath, fileName: fileName, index: index });
            }
        }
        MenuItem {
            text: qsTr("Delete")
            onClicked: {
              deleteQueryDialog.index = index;

              deleteQueryDialog.fileName = fileName;
              deleteQueryDialog.open();
            }
        }
    }
}
