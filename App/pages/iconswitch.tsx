import React, { useRef, useEffect } from 'react';
import { TouchableOpacity, View, StyleSheet, Animated } from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

interface IconSwitchProps {
  value: boolean;
  onValueChange: () => void;
}

const IconSwitch: React.FC<IconSwitchProps> = ({ value, onValueChange }) => {
  const position = useRef(new Animated.Value(value ? 1 : 0)).current;

  useEffect(() => {
    Animated.timing(position, {
      toValue: value ? 1 : 0,
      duration: 300,
      useNativeDriver: false,
    }).start();
  }, [value]);

  const translateX = position.interpolate({
    inputRange: [0, 1],
    outputRange: [0, 50],  // Adjust the output range based on your switch width
  });

  return (
    <TouchableOpacity onPress={onValueChange} style={styles.switchContainer}>
      <Animated.View style={[styles.iconContainer, { transform: [{ translateX }] }]}>
        <Icon name={value ? "close" : "check"} size={48} color="black" />
      </Animated.View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  switchContainer: {
    top: 80,
    width: 140,
    height: 100,
    borderRadius: 100,
    backgroundColor: 'grey',
    justifyContent: 'center',
    padding: 5,
  },
  iconContainer: {
    width: 90,
    height: 90,
    borderRadius: 100,
    backgroundColor: 'white',
    justifyContent: 'center',
    alignItems: 'center',
    position: 'absolute',
  },
});

export default IconSwitch;
