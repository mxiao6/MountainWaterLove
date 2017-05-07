using UnityEngine;
using System.Collections;

public class playMusic : MonoBehaviour {

	public float delayTime;

	private AudioSource audioSource;

	// Use this for initialization
	void Start () {
		audioSource = GetComponent<AudioSource>();
		audioSource.PlayDelayed( delayTime );
	}
	
	// Update is called once per frame
	// void Update () {
	
	// }
}
