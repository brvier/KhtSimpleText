import QtQuick 1.1
import com.nokia.meego 1.0
import com.nokia.extras 1.1
import 'components'
import 'common.js' as Common

PageStackWindow {
    id: appWindow

    initialPage: fileBrowserPage

    MainPage {
        id: fileBrowserPage
    }

    NewFilePage {
        id: newFilePage
    }
    CopyFilePage {
        id: copyFilePage
    }
    MoveFilePage {
        id: moveFilePage
    }

    NewFolderPage {
        id: newFolderPage
    }

    EditPage {
        id: fileEditPage
    }

    PreviewPage {
        id: previewPage
    }

    RenamePage {
        id: renameFilePage
    }

    ItemMenu {
        id: itemMenu
    }

    ToolBarLayout {
        id: mainTools
        visible: true
        ToolIcon {
            platformIconId: "toolbar-view-menu"
            anchors.right: (parent === undefined) ? undefined : parent.right
            onClicked: (myMenu.status === DialogStatus.Closed) ? myMenu.open() : myMenu.close()
        }
    }


    ToolBarLayout {
        id: commonTools
        visible: false
        ToolIcon {
            platformIconId: "toolbar-back"
            anchors.left: (parent === undefined) ? undefined : parent.left
            onClicked: pageStack.pop();
        }
        ToolIcon {
            platformIconId: "toolbar-view-menu"
            anchors.right: (parent === undefined) ? undefined : parent.right
            onClicked: (myMenu.status === DialogStatus.Closed) ? myMenu.open() : myMenu.close()
        }
    }


    Menu {
        id: myMenu
        visualParent: pageStack
        MenuLayout {
            MenuItem { text: qsTr("About"); onClicked: about.open()}
            MenuItem { text: qsTr("New File"); onClicked: {
                       pageStack.push(newFilePage, {filePath: fileBrowserPage.currentFolder});
                       }
            }
            MenuItem { text: qsTr("New Folder");onClicked: {
                       pageStack.push(newFolderPage, {filePath: fileBrowserPage.currentFolder});
                       }
            }
            /*MenuItem { text: qsTr("Preferences"); onClicked: notYetAvailableBanner.show(); }*/
        }
    }

    InfoBanner{
                      id:notYetAvailableBanner
                      text: 'This feature is not yet available'
                      timerShowTime: 5000
                      timerEnabled:true
                      anchors.top: parent.top
                      anchors.topMargin: 60
                      anchors.horizontalCenter: parent.horizontalCenter
                 }

    InfoBanner{
                      id:errorBanner
                      text: 'An error occur while creating new folder'
                      timerShowTime: 15000
                      timerEnabled:true
                      anchors.top: parent.top
                      anchors.topMargin: 60
                      anchors.horizontalCenter: parent.horizontalCenter
                 }

    function onError(errMsg) {
        errorEditBanner.text = errMsg;
        errorEditBanner.show();
    }

    InfoBanner{
                      id:errorEditBanner
                      text: ''
                      timerShowTime: 15000
                      timerEnabled:true
                      anchors.top: parent.top
                      anchors.topMargin: 60
                      anchors.horizontalCenter: parent.horizontalCenter
                 }

   showStatusBar: true

    QueryDialog {
        property string filepath
        id: deleteQueryDialog
        icon: Qt.resolvedUrl('../icons/khtsimpletext.png')
        titleText: "Delete"
        message: "Are you sure you want to delete : " + Common.beautifulPath(filepath) + '?'
        acceptButtonText: qsTr("Delete")
        rejectButtonText: qsTr("Cancel")
        onAccepted: {
                if (!(QmlDirReaderWriter.rm(filepath))) {
                    errorBanner.text = 'An error occur while deleting item';
                    errorBanner.show();
                }
                else {fileBrowserPage.refresh();}
        }
    }

    /*Dialog {
               id: newDialog
               title: Label {text:'New file name :'; color: 'white'; }

               content: Item {
                   height: 100
                   anchors {left: parent.left; right: parent.right; verticalCenter:parent.verticalCenter}
                   TextField {
                   id: newDialogTextField
                   anchors {left: parent.left; right: parent.right; verticalCenter:parent.verticalCenter}
                   maximumLength: 60
                   height: 50
                   focus: true
                }
               }

                buttons: Row {
                   anchors.horizontalCenter: parent.horizontalCenter
                   spacing: 30
                   Button {
                       text: "Create";
                       onClicked: {
                            newDialog.accept();
                            pageStack.push(fileEditPage, { filePath: fileBrowserPage.currentFolder + '/' +newDialogTextField.text });
                       }
                   }
                   Button {
                       anchors.topMargin: 40
                       text: "Cancel"; onClicked: newDialog.reject()
                   }}
     }*/

    QueryDialog {
                id: about
                icon: Qt.resolvedUrl('../icons/khtsimpletext.png')
                titleText: "About KhtSimpleText"
                message: 'Version ' + __version__ +
                         '\nBy Benoît HERVIER (Khertan)\n' +
                         '\n\nA simple plain text editor for MeeGo and Harmattan\n' +
                         'Licenced under GPLv3\n' +
                         'Web Site : http://khertan.net/khtsimpletext'
                }


    states: [
            State {
                        name: "fullsize-visible"
                        when: platformWindow.viewMode == WindowState.Fullsize && platformWindow.visible
                        StateChangeScript {
                                 script: {
                                 console.log("Visibility: Fullsize and visible!");
                                 pageStack.currentPage.refresh();
                                 }       }
                  }
            ]
}
