using UnityEngine;
using System.Collections;

public class playMusic : MonoBehaviour {

	private AudioSource audioSource;

	// Use this for initialization
	void Start () {
		audioSource = GetComponent<AudioSource>();
		DontDestroyOnLoad(audioSource);
	}
	
	// Update is called once per frame
	// void Update () {
	
	// }
}
