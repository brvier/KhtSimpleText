import QtQuick 1.1
import com.nokia.meego 1.0
import "components"
import 'common.js' as Common

Page {
    id: root

    property string filePath;

    tools: commonTools

    PageHeader {
        id: header
        title: 'KhtSimpleText : New Folder'
        subtitle: Common.beautifulPath(filePath);
    }

    Column {
        anchors.top: header.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.margins: 12
        spacing: 12

        Label {
            text: "New folder"
        }

        TextField {
            id: inputField
            anchors.left: parent.left
            anchors.right: parent.right
            placeholderText: "Folder name"
        }

        Button {
            anchors.left: parent.left
            anchors.right: parent.right
            enabled: inputField.text != ""
            text: "Create folder"
            onClicked: {
                pageStack.pop();
                if (!QmlFileReaderWriter.newFolder(filePath + inputField.text)) {
                      errorBanner.text = 'An error occur while creating new folder';
                      errorBanner.show();}
            }
        }
    }
}
