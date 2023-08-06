import QtQuick 2.7
import org.kde.kirigami 2.5 as Kirigami
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3
import GHPhysicalActivity 0.1

Kirigami.Page {

    id: physicalactivityPage
    title: qsTr("Physical Activity")

    // font.pointSize: Kirigami.Theme.defaultFont.pointSize * 2

    GHPhysicalActivity { // PhysicalActivity object registered at mygh.py
        id: physicalactivity
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
        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter
        color: "#136f84"
        height: 80
        width: parent.width
        radius: 10
        Image {
            id: activityIcon
            height: parent.height* 0.9
            anchors.centerIn: parent
            source: "../images/steps-icon.svg"
            fillMode: Image.PreserveAspectFit
        }
    }
    ColumnLayout {
        anchors.centerIn: parent
        Layout.alignment: Qt.AlignHCenter

        id: pagrid
        Label {
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Aerobic (minutes)")
            font.bold: true
        }

        SpinBox {
            id: paAerobic
            Layout.preferredHeight: 80
            Layout.preferredWidth: 120
            Layout.alignment: Qt.AlignHCenter
            font.pixelSize:30
            from: 0
            to: 600
            editable: true
            inputMethodHints: Qt.ImhDigitsOnly
            wheelEnabled: true
         }

        Label {
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Anaerobic (minutes)")
            font.bold: true
        }

        SpinBox {
            id: paAnaerobic
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredHeight: 80
            Layout.preferredWidth: 120
            font.pixelSize:30
            from: 0
            to: 600
            editable: true
            inputMethodHints: Qt.ImhDigitsOnly
            wheelEnabled: true
         }

        Label {
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Steps")
            font.bold: true
        }

        Slider {
            id: sliderpa
            Layout.alignment: Qt.AlignHCenter
            from: 0
            to: 100000
            stepSize: 1
            wheelEnabled: true
        }

         TextField {
            id: paSteps
            Layout.alignment: Qt.AlignHCenter
            placeholderText: qsTr("Steps")
            horizontalAlignment: Text.AlignHCenter
            text: sliderpa.value
            inputMethodHints: Qt.ImhDigitsOnly
            onEditingFinished: sliderpa.value = Number(paSteps.text)
            font.bold: true
        }

        Button {
            id: buttonSetPA
            Layout.columnSpan: 2
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Set")
            flat: false
            onClicked: {
                physicalactivity.getvals(paAerobic.value, paAnaerobic.value,
                                        sliderpa.value);
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

