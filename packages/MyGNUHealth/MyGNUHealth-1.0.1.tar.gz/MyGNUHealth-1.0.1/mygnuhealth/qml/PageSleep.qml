import QtQuick 2.7
import org.kde.kirigami 2.5 as Kirigami
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3
import GHSleep 0.1

Kirigami.Page {

    id: sleepPage
    title: qsTr("Sleep")

    // font.pointSize: Kirigami.Theme.defaultFont.pointSize * 2

    GHSleep { // PhysicalActivity object registered at mygh.py
        id: sleep
        onSetOK: {
            /* We pop the current page from the stack and immediately
            /  replace the LifeStyle page to refresh its contents
            */
            pageStack.pop()
            pageStack.replace(Qt.resolvedUrl("PageLifestyle.qml"))
        }
    }

    Rectangle
        {
        id: rectheader
        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter
        color: "#136f84"
        height: 80
        width: parent.width
        radius: 10
        Image {
            id: sleepIcon
            height: parent.height* 0.9
            anchors.centerIn: parent
            source: "../images/sleep-icon.svg"
            fillMode: Image.PreserveAspectFit
        }
    }

    ColumnLayout {
        anchors.centerIn: parent

        id: sleepgrid
        Label {
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Sleep hours")
        }

        SpinBox {
            id: sleepHours
            Layout.preferredHeight: 60
            Layout.preferredWidth: 120
            Layout.alignment: Qt.AlignHCenter
            font.pixelSize:30
            from: 0
            to: 24
            editable: true
            inputMethodHints: Qt.ImhDigitsOnly
            wheelEnabled: true
         }

        ComboBox {
            id: sleepQuality
            Layout.alignment: Qt.AlignHCenter
            textRole: "text"
            valueRole: "value"
            model: [
                { value: "good", text: qsTr("Good") },
                { value: "light", text: qsTr("Light") },
                { value: "poor", text: qsTr("Poor") }
            ]
        }

        TextArea {
            id:information
            Layout.preferredWidth: rectheader.width
            Layout.preferredHeight: 100
            placeholderText: qsTr("Enter details here")
            wrapMode: TextEdit.WordWrap
        }


        Button {
            id: buttonSetSleep
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Set")
            flat: false
            onClicked: {
                sleep.getvals(sleepHours.value, sleepQuality.currentValue,
                                  information.text);
            }
        }      

    }
   footer: Rectangle{
            id: rectfooter
            width: parent.width
            height: 40
            Image {
                id: myghIcon
                anchors.centerIn: rectfooter
                source: "../images/myGH-horizontal-icon.svg"
                width: 160
                fillMode: Image.PreserveAspectFit
            }
        }

}

