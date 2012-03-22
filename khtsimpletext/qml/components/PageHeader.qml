import QtQuick 1.1
import com.nokia.meego 1.0

    Rectangle {
        id:header

        property alias title: headerlabel.text
        property alias subtitle: headerpathlabel.text

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
            text:''
        }
    }