import QtQuick 1.1
import com.nokia.meego 1.0
import 'components'
import 'common.js' as Common

Page {
    tools: mainTools

    signal refresh();
    
    onRefresh: {
	DocumentsModel.loadDir();
    }
   
        
    PageHeader {
         id: header
         title: 'KhtSimpleText'
         subtitle: Common.beautifulPath(DocumentsModel.currentpath);
    }

    ListView {

        id: fileView
        anchors.top: header.bottom
        anchors.bottom: parent.bottom

        height: parent.height - header.height
        width: parent.width
        z:1

        model:DocumentsModel

        Component {
            id: fileDelegate
            Rectangle {
                width:parent.width
                height: 80
                anchors.leftMargin: 10
                color:"white"

                Rectangle {
                    id: background
                    anchors.fill: parent
                    color: "darkgray";
                    opacity: 0.0 
                    Behavior on opacity { NumberAnimation {} }
                }

                Column {
                    spacing: 10
                    anchors.leftMargin:10
                    anchors.left: parent.left
                    anchors.right: moreIcon.left
                    anchors.verticalCenter: parent.verticalCenter
                    Label {text:'<b>'+filename+'</b>'
                        font.family: "Nokia Pure Text"
                        font.pixelSize: 24
                        color:"black"
                        anchors.left: parent.left
                        anchors.right: parent.right
                    }

                    Label {
                        text: Common.beautifulPath(filepath);
                        font.family: "Nokia Pure Text"
                        font.pixelSize: 16
                        color: "#cc6633"
                        anchors.left: parent.left;
                        anchors.right: parent.right
                        elide: Text.ElideRight
                        maximumLineCount: 1
                        }
                }

                Image {
                    id:moreIcon
                    source: "image://theme/icon-m-common-drilldown-arrow"
                    anchors.right: parent.right;
                    anchors.rightMargin: 5
                    anchors.verticalCenter: parent.verticalCenter
                    opacity: isdir ? 1.0 : 0.0
                }

                MouseArea {
                    anchors.fill: parent
                    onPressed: background.opacity = 1.0;
                    onReleased: background.opacity = 0.0;
                    onPositionChanged: background.opacity = 0.0;

                    onClicked: {
                        console.log(filepath)
                        if (isdir) {
                            DocumentsModel.currentpath  = filepath
                        }
                        else {
                            var editingPage = Qt.createComponent(Qt.resolvedUrl("EditPage.qml"));
                            Document.filepath = filepath;
                            Document.load();
                            pageStack.push(editingPage, {index: index, 
                                                         modified: false});
                        }
                    }
                    onPressAndHold: {
                        itemMenu.filePath = filepath;
                        itemMenu.fileName = filename;
//                        itemMenu.pageStack = appWindow;
                        itemMenu.open();
                   }
                }
            }
        }
        delegate: fileDelegate

    }

  ScrollDecorator {
        flickableItem: fileView
        z:3
        platformStyle: ScrollDecoratorStyle {
        }}

    onStatusChanged: {
         if (status == PageStatus.Active) {
              DocumentsModel.loadDir();
         }
    }

}
