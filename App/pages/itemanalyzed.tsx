import React, { useEffect } from 'react';
import { View, Text, StyleSheet, Image, ImageBackground, TouchableOpacity } from 'react-native';
import { Button, Modal, Portal, Provider as PaperProvider } from 'react-native-paper';
import { useItem } from '../context/ItemContext';
import { NavigationProp } from '@react-navigation/native';
import axios from 'axios';
import IconSwitch from './iconswitch';

interface ItemAnalyzedProps {
  navigation: NavigationProp<any>;
}

export default function ItemAnalyzed({ navigation }: ItemAnalyzedProps) {
  const { item } = useItem();
  const [visible, setVisible] = React.useState(false);
  const [buttonText, setButtonText] = React.useState('Continue');
  const [rightObject, setRightObject] = React.useState(true);


  

  

  const onToggleSwitch = () => setRightObject(!rightObject);

  const cancleStory = async () => {
    navigation.navigate('Start');
  }

  useEffect(() => {
    setButtonText(rightObject ? "Try again" : "Continue");
  }, [rightObject]);

  const handlePress = async () => {
    try {
      if (!rightObject) {
        navigation.navigate('PutHeadphonesOn');
      } else {
        setButtonText("Try again");
        showModal();
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const showModal = () => setVisible(true);
  const hideModal = () => setVisible(false);

  const containerStyle = {
    backgroundColor: 'black',
    padding: 20,
    height: '60%',
    width: '90%',
    borderRadius: 20,
    alignSelf: 'center',
  };

  return (
    <PaperProvider>
      <ImageBackground 
        source={require('../images/decor4.png')} 
        style={styles.container}
      >
        <Text style={styles.reflectYourCycle}>
          {item}
          {'\n'}
          analyzed
        </Text>


        <IconSwitch value={rightObject} onValueChange={onToggleSwitch} />

        <Portal>
          <Modal visible={visible} onDismiss={hideModal} contentContainerStyle={[containerStyle, { zIndex: 100 }]}>
            <Text style={styles.modalText}>
              Before cancelling the currently played story, please make sure, the installation is really empty!
            </Text>
            <View style={styles.buttonContainer}>
              <Text style={styles.modalSubText}>
                Are you sure you want to stop the installation?
              </Text>
              <Button mode="contained" onPress={cancleStory} style={styles.modalButton} labelStyle={styles.modalButtonLabel}>
                Yes, Stop
              </Button>
              <TouchableOpacity onPress={hideModal}>
                <Text style={styles.closeModalText}>
                  No, keep running
                </Text>
              </TouchableOpacity>
            </View>
          </Modal>
        </Portal>
        <View style={styles.buttonContainerAbsolute}>
          <Button
            mode="contained"
            onPress={handlePress}
            style={styles.button}
            labelStyle={styles.buttonLabel}
          >
            {buttonText}          
          </Button>
        </View>
      </ImageBackground>
    </PaperProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#000',
  },
  reflectYourCycle: {
    position: 'absolute',
    top: '15%',
    color: '#fff',
    fontFamily: '',
    fontSize: 18,
    letterSpacing: 14.4,
    lineHeight: 57.6,
    textAlign: 'center',
    textTransform: 'uppercase',
  },
  image: {
    width: 100,
    height: 100,
    position: 'absolute',
    top: '40%',
  },
  button: {
    width: '80%',
    height: 64,
    backgroundColor: '#D7D3DB',
    justifyContent: 'center',
    marginVertical: 10,
  },
  buttonLabel: {
    color: 'black',
    fontFamily: '',
    fontSize: 20,
    textTransform: 'uppercase',
  },
  buttonContainerAbsolute: {
    position: 'absolute', 
    bottom: "8%", 
    justifyContent: 'center',
    alignItems: 'center',
    width: '100%',
  },
  buttonContainer: {
    justifyContent: 'center',
    alignItems: 'center',
    width: '100%',
  },
  modalText: {
    color: 'white',
    fontFamily: '',
    fontSize: 24,
    textAlign: 'center',
  },
  modalSubText: {
    color: 'white',
    fontFamily: '',
    fontSize: 24,
    textAlign: 'center',
    marginVertical: 20,
  },
  modalButton: {
    width: '80%',
    height: 64,
    backgroundColor: '#D7D3DB',
    justifyContent: 'center',
    marginVertical: 10,
  },
  modalButtonLabel: {
    color: 'black',
    fontFamily: '',
    fontSize: 20,
    textTransform: 'uppercase',
  },
  closeModalText: {
    color: 'white',
    fontFamily: '',
    fontSize: 18,
    textAlign: 'center',
    textDecorationLine: 'underline',
    marginTop: 20,
  },
});
