
clickcounter.h
#ifndef CLICKCOUNTER_H
#define CLICKCOUNTER_H

#include <QWidget>
class QLabel ;
class QPushButton ;
class QVBoxLayout ;

class Counter : public QWidget {
    Q_OBJECT
public :
   Counter( QWidget * parent = 0 ) ;
private :
   int number ;
   QLabel *countLabel ;
   QPushButton *clicker ;
   QVBoxLayout *myLayout ;
private slots :
   void countClicks( ) ;
} ;
#endif

clickcounter.cpp
#include <QPushButton>
#include <QLabel>
#include <QVBoxLayout>
#include "clickcounter.h" 

Counter::Counter( QWidget * parent ) : QWidget( parent ) {
   number = 0 ;
   countLabel = new QLabel( "There have been no clicks yet!" ) ;
   clicker = new QPushButton( "click me" ) ;
   connect ( clicker , SIGNAL( clicked( ) ) , this , SLOT( countClicks( ) ) ) ;
   myLayout = new QVBoxLayout ;
   myLayout->addWidget( countLabel ) ;
   myLayout->addWidget( clicker ) ;
   setLayout( myLayout ) ;
}

void Counter::countClicks( ) {
   number++ ;
   countLabel->setText( QString( "The button has been clicked %1 times!").arg( number ) ) ;
}

main.cpp
#include <QApplication>
#include "clickcounter.h"

int main( int argc , char *argv[ ] ) {
   QApplication app( argc , argv ) ;
   Counter counter ;
   counter.show( ) ;
   return app.exec( ) ;
}
