import QtQuick 1.1
import com.nokia.meego 1.0
import "components"
import 'common.js' as Common

Page {
    id: root

    property string filePath;
    property string fileName;
    property int index;

    tools: commonTools

    PageHeader {
        id: header
        title: 'KhtSimpleText : Rename'
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
            text: 'Rename ' + Common.beautifulPath(filePath) + ' to :'
        }

        TextField {
            id: inputField
            anchors.left: parent.left
            anchors.right: parent.right
            placeholderText: fileName
            text: fileName
        }

        Button {
            anchors.left: parent.left
            anchors.right: parent.right
            enabled: inputField.text != ""
            text: "Rename"
            onClicked: {
                pageStack.pop();
                if (!DocumentsModel.rename(index, inputField.text)) {
                      errorBanner.text = 'An error occur while renaming file';
                      errorBanner.show();}
            }
        }
    }
}
