import { View, Text, Image, StyleSheet } from 'react-native';
import React, { useEffect } from 'react';
import StopinstallationButton from '../compontens/StopinstallationButton';
import { NavigationProp } from '@react-navigation/native';

interface ItemAnalyzedProps {
    navigation: NavigationProp<any>;
  }

export default function EnterRoom({ navigation } : ItemAnalyzedProps ) {
    const [changeScreen, setChangeScreen] = React.useState(false);

    useEffect(() => {
        const timer = setTimeout(() => {
            if (changeScreen === false) {
                navigation.navigate('CurrentlyUsed');
            }
        }, 30000);
        return () => clearTimeout(timer);
    }, [navigation]);



    return (

        <View style={styles.container}>
            <StopinstallationButton setScreen={setChangeScreen}/>  
            <Image 
                source={require('../images/decor5.png')} 
                style={styles.image} 
                resizeMode="contain"
            />
            <View style={styles.box}>
                <View style={styles.group}>
                    <View style={styles.overlapGroup}>
                        <Text style={styles.reflectYourCycle}>
                            Please enter
                            {'\n'}
                            the room now
                            {'\n'}
                            and learn about your product
                        </Text>
                    </View>
                </View>
            </View>
        </View>

    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#000',
        alignItems: 'center',
    },
    image: {
        width: '100%', 
    },
    box: {
        width: 320,
    },
    group: {
        position: 'absolute',  
        height: 211,
        width: '100%',
    },
    overlapGroup: {
        height: 211,
        width: '100%',
    },
    reflectYourCycle: {
        position: 'absolute', 
        bottom: '8%', 
        color: '#fff',
        fontFamily: '',
        fontSize: 18,
        letterSpacing: 14.4,
        lineHeight: 57.6,
        textAlign: 'center',
        textTransform: 'uppercase',
        width: '100%',
    }
});