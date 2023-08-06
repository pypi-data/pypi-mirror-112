import QtQuick 2.7
import org.kde.kirigami 2.5 as Kirigami
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3
import BloodPressure 0.1

Kirigami.Page {

    id: bloodpressurePage
    title: qsTr("Blood Pressure")


    BloodPressure { // BloodPressure object registered at mygh.py
        id: bloodpressure
        onSetOK: {
            /* We pop the current page from the stack and immediately
            /  replace the Biopage to refresh its contents
            */
            pageStack.pop()
            pageStack.replace(Qt.resolvedUrl("PageBio.qml"))
        }
    }

    Rectangle {
        id: rectheader
        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter
        color: "#136f84"
        height: 80
        width: parent.width
        radius: 10
        Image {
            id: bpIcon
            height: parent.height
            anchors.centerIn: parent
            source: "../images/bp-icon.svg"
            fillMode: Image.PreserveAspectFit
        }
    }

    ColumnLayout {
        id: bpgrid
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: rectheader.bottom
        anchors.topMargin: 50

        Label {
            text: qsTr("Systolic Pressure")
            Layout.alignment: Qt.AlignHCenter
            font.bold: true
        }
        SpinBox {
            id: txtSystolic
            Layout.preferredHeight: 80
            Layout.preferredWidth: 150
            font.pixelSize:30
            from: 0
            to: 300
            value: 120
            editable: true
            inputMethodHints: Qt.ImhDigitsOnly
            wheelEnabled: true
         }
        Label {
            text: qsTr("Diastolic Pressure")
            Layout.alignment: Qt.AlignHCenter
            font.bold: true
        }
        SpinBox {
            id: txtDiastolic
            Layout.preferredHeight: 80
            Layout.preferredWidth: 150
            font.pixelSize:30
            from: 0
            to: 250
            value: 80
            editable: true
            inputMethodHints: Qt.ImhDigitsOnly
            wheelEnabled: true
        }
        Text {
            text: qsTr("Heart Rate")
            Layout.alignment: Qt.AlignHCenter
            font.bold: true
        }
        SpinBox {
            id: txtRate
            Layout.preferredHeight: 80
            Layout.preferredWidth: 150
            font.pixelSize:30
            from: 0
            to: 300
            value: 72
            editable: true
            inputMethodHints: Qt.ImhDigitsOnly
            wheelEnabled: true
        }

        Button {
            id: buttonSetBP
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Set")
            flat: false
            onClicked: {
                bloodpressure.getvals(txtSystolic.value, txtDiastolic.value,
                                        txtRate.value);
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

