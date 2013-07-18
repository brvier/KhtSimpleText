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
        title: 'KhtSimpleText : New File'
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
            text: "New file"
        }

        TextField {
            id: inputField
            anchors.left: parent.left
            anchors.right: parent.right
            placeholderText: "File name"
        }

        Button {
            anchors.left: parent.left
            anchors.right: parent.right
            enabled: inputField.text != ""
            text: "Create file"
            onClicked: {
                var index = DocumentsModel.newFile(inputField.text);
                if (index >= 0) {
                    Document.filepath = DocumentsModel.currentpath + '/' + inputField.text;
                    Document.load();
                    replaceWithEdit(index);}
                else {
                    onError(inputField.text + ' already exists');                    
                }
                
            }
        }
    }
} 