import QtQuick 1.1
import com.nokia.meego 1.0
import 'components'
import 'common.js' as Common

Page {
    tools: simpleBackTools
    id: settingsPage

    signal refresh();

    onRefresh: {
    }

    function exitFile() {
        pageStack.pop();
    }

    PageHeader {
        id: header
        title: 'KhtSimpleText'
    }


    Flickable {
        id: flick
        interactive: true
        anchors.top: header.bottom
        anchors.right: parent.right
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        contentWidth: parent.width
        contentHeight: settingsColumn.height + 30
        clip: true

        Column {
            id: settingsColumn
            spacing: 10
            width: parent.width - 40
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
            anchors.topMargin: 20
            
            TitleLabel {
                text: qsTr("Appearance")
            }

            Label {
                text: qsTr("Hide Header")
                width: parent.width
                height: displayHeaderSwitch.height
                verticalAlignment: Text.AlignVCenter
                Switch {
                    id: displayHeaderSwitch
                    anchors.right: parent.right
                    checked: Settings.hideHeader
                    Binding {
                        target: Settings
                        property: "hideHeader"
                        value: displayHeaderSwitch.checked
                    }
                }
            }

            Label {
                text: qsTr("Font size")
                width: parent.width
                height: fontSlider.height
                verticalAlignment: Text.AlignVCenter
                Slider {
                    id: fontSlider
                    minimumValue: 9
                    maximumValue: 40
                    stepSize: 1
                    width: 300
                    valueIndicatorVisible: true
                    value: Settings.fontSize
                    anchors.right: fontSliderLabel.left
                    Binding {
                        target: Settings
                        property: "fontSize"
                        value: fontSlider.value
                    }
                }
                Label {
                    id: fontSliderLabel
                    text: fontSlider.value
                    width: 50
                    anchors.right: parent.right
                    anchors.verticalCenter: parent.verticalCenter
                }
            }
            
            TitleLabel {
                text: qsTr('Virtual Keyboard')
            }

            Label {
                width: parent.width
                height: hideVkbSwitch.height
                verticalAlignment: Text.AlignVCenter
                text: qsTr("Hide")

                Switch {
                    id: hideVkbSwitch
                    checked: Settings.hideVKB
                    anchors.right: parent.right
                    Binding {
                        target: Settings
                        property: "hideVKB"
                        value: hideVkbSwitch.checked
                    }
                }
            }
                        
            TitleLabel {
                text: qsTr('Editor')
            }


            /*Label {
                width: parent.width
                height: wrapSwitch.height
                verticalAlignment: Text.AlignVCenter
                text: qsTr("Wrap text")

                Switch {
                    id: wrapSwitch
                    checked: Settings.textWrap
                    anchors.right: parent.right
                    Binding {
                        target: Settings
                        property: "textWrap"
                        value: wrapSwitch.checked
                    }
                }
            }*/

            Label {
                width: parent.width
                height: syntaxSwitch.height
                verticalAlignment: Text.AlignVCenter
                text: qsTr("Use syntax highlighting")

                Switch {
                    id: syntaxSwitch
                    checked: Settings.syntaxHighlighting
                    anchors.right: parent.right
                    Binding {
                        target: Settings
                        property: "syntaxHighlighting"
                        value: syntaxSwitch.checked
                    }
                }
            }

            TitleLabel {
                text: qsTr('Folder Browser')
            }

            Label {
                width: parent.width
                height: lastPositionSwitch.height
                verticalAlignment: Text.AlignVCenter
                text: qsTr("Save last position")

                Switch {
                    id: lastPositionSwitch
                    checked: Settings.useLastOpenedFolder
                    anchors.right: parent.right
                    Binding {
                        target: Settings
                        property: "useLastOpenedFolder"
                        value: lastPositionSwitch.checked
                    }
                }
            }
        }
    }

    ScrollDecorator {
        flickableItem: flick
        platformStyle: ScrollDecoratorStyle {
        }}

    Menu {
        id: editMenu
        visualParent: pageStack
        MenuLayout {
            MenuItem { text: qsTr("About"); onClicked: pushAbout()}
        }
    }

    ToolBarLayout {
        id: simpleBackTools
        visible: true
        ToolIcon {
            platformIconId: "toolbar-back"
            anchors.left: (parent === undefined) ? undefined : parent.left
            onClicked: {
                pageStack.pop();
            }
        }

        ToolIcon {
            platformIconId: "toolbar-view-menu"
            anchors.right: (parent === undefined) ? undefined : parent.right
            onClicked: (editMenu.status === DialogStatus.Closed) ? editMenu.open() : editMenu.close()
        }
    }
}  