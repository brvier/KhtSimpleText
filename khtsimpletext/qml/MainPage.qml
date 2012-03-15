import QtQuick 1.1
import com.nokia.meego 1.0
import Qt.labs.folderlistmodel 1.0
import 'components'

Page {
    tools: commonTools

    property string currentFolder;
    signal refresh();
    
    onRefresh: {
	folderModel.nameFilters = '*';
    }
    
    PageHeader {
         id: header
         title: 'KhtSimpleText'
         subtitle: folderModel.folder
    }

    ListView {

        id: fileView
        anchors.top: header.bottom
        anchors.bottom: parent.bottom

        height: parent.height - header.height
        width: parent.width
        z:1

        FolderListModel {
            id: folderModel
            folder: '~'
            showDotAndDotDot : true
        }

        Component {
            id: fileDelegate
            Rectangle {
                width:parent.width
                height: 80
                anchors.leftMargin: 10
                color:"white"

                Column {
                    spacing: 10
                    anchors.leftMargin:10
                    anchors.left: parent.left
                    anchors.right: moreIcon.left
                    anchors.verticalCenter: parent.verticalCenter
                    Label {text:'<b>'+fileName+'</b>'
                        font.family: "Nokia Pure Text"
                        font.pixelSize: 24
                        color:"black"
                        anchors.left: parent.left
                        anchors.right: parent.right
                    }

                    Label {text:filePath
                        font.family: "Nokia Pure Text"
                        font.pixelSize: 16
                        color: "#cc6633"
                        anchors.left: parent.left;
                        anchors.right: parent.right
                    }
                }

                Image {
                    id:moreIcon
                    source: "image://theme/icon-m-common-drilldown-arrow"
                    anchors.right: parent.right;
                    anchors.rightMargin: 5
                    anchors.verticalCenter: parent.verticalCenter
                    opacity: folderModel.isFolder(index)
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        console.log(filePath)
                        if (folderModel.isFolder(index)) {
                            folderModel.folder  = filePath
                            currentFolder = filePath
                        }
                        else {
                             pageStack.push(fileEditPage, { filePath: filePath });
                        }
                    }
                    onPressAndHold: {
                        itemMenu.item = filePath
                        itemMenu.open();
                   }
                }
            }
        }
        model: folderModel
        delegate: fileDelegate

    }

  ScrollDecorator {
        flickableItem: fileView
        z:3
        platformStyle: ScrollDecoratorStyle {
        }}

    onStatusChanged: {
         if (status == PageStatus.Active) {
              folderModel.nameFilters = '*';
         }
    }

}
