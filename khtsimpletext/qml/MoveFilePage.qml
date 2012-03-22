import QtQuick 1.1
import com.nokia.meego 1.0
import "components"
import 'common.js' as Common

Page {
    id: root

    property string filePath;
    property string fileName;

    tools: commonTools

    PageHeader {
        id: header
        title: 'KhtSimpleText : Move File'
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
            text: "Move file " + Common.beautifulPath(filePath) + ' to :'
        }

        TextField {
            id: inputField
            anchors.left: parent.left
            anchors.right: parent.right
            placeholderText: filePath
            text: filePath
        }

        Button {
            anchors.left: parent.left
            anchors.right: parent.right
            enabled: inputField.text != ""
            text: "Create file"
            onClicked: {
                pageStack.pop()
                if (!QmlFileReaderWriter.mv(inputField.text)) {
                      errorBanner.text = 'An error occur while moving file';
                      errorBanner.show();}
            }
        }
    }
}
