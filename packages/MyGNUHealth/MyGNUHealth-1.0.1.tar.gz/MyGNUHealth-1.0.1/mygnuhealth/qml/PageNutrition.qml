import QtQuick 2.7
import org.kde.kirigami 2.5 as Kirigami
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3
import GHNutrition 0.1

Kirigami.Page {

    id: nutritionPage
    title: qsTr("Nutrition")

    // font.pointSize: Kirigami.Theme.defaultFont.pointSize * 2

    GHNutrition { // GHNutrition object registered at mygh.py
        id: nutrition
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
            id: nutritionIcon
            height: parent.height* 0.9
            anchors.centerIn: parent
            source: "../images/nutrition-icon.svg"
            fillMode: Image.PreserveAspectFit
        }
    }

    ColumnLayout {
        id: nutrigrid
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: rectheader.bottom
        anchors.topMargin: 20

        Label {
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Morning")
        }
        SpinBox {
            id: nutriMorning
            Layout.preferredHeight: 60
            Layout.preferredWidth: 150
            Layout.alignment: Qt.AlignHCenter
            font.pixelSize:30
            from: 0
            to: 5000
            editable: true
            inputMethodHints: Qt.ImhDigitsOnly
            wheelEnabled: true
         }

        Label {
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Afternoon")
        }

        SpinBox {
            id: nutriAfternoon
            Layout.preferredHeight: 60
            Layout.preferredWidth: 150
            Layout.alignment: Qt.AlignHCenter
            font.pixelSize:30
            from: 0
            to: 5000
            editable: true
            inputMethodHints: Qt.ImhDigitsOnly
            wheelEnabled: true
         }

        Label {
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Evening")
        }

        SpinBox {
            id: nutriEvening
            Layout.preferredHeight: 60
            Layout.preferredWidth: 150
            Layout.alignment: Qt.AlignHCenter
            font.pixelSize:30
            from: 0
            to: 5000
            editable: true
            inputMethodHints: Qt.ImhDigitsOnly
            wheelEnabled: true
         }

        Label {
            id: nutriTotal
            Layout.alignment: Qt.AlignHCenter
            font.bold: true
            property int kcal: Number(nutriMorning.value + nutriAfternoon.value + nutriEvening.value)
            text: qsTr("Total Kcal:") + " " + kcal
        }

        TextArea {
            id:information
            Layout.fillWidth: true
            Layout.preferredHeight: 100
            Layout.preferredWidth: rectheader.width
            placeholderText: qsTr("Enter details here")
        }


        Button {
            id: buttonSetNutrition
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Set")
            flat: false
            onClicked: {
                nutrition.getvals(nutriMorning.value, nutriAfternoon.value,
                                         nutriEvening.value, nutriTotal.kcal,
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

