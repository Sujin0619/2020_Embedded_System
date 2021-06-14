# 2020_Embedded_System

#### <라즈베리파이를 이용한 OLED 콘솔 게임>

##### Starcrft vs Alien 게임은 SSD1306 display에 2D animation을 띄워서 만든 게임으로, 라즈베리파이의 GPIO pin들 중 총 4개를 게임 조작 버튼으로 사용했다. 플레이어는 starcraft가 되어 Alien을 공격하여 우주를 구한다. 총 세 단계로 이루어지며, 모든 단계에서 Alien을 상대로 승리해야만 진정한 starcrafter가 될 수 있다.


##### Level에 따라 Player, Alien이 한 화면 안에서 쏠 수 있는 bullet의 수가 달라진다. 또한, 시간제한과 생명의 개수도 달라진다.  


##### 1. Start Page : 가장 왼쪽의 Start_pin을 누르면 게임이 시작되며, Player가 게임을 그만하겠다고 Quit 버튼을 누르면 돌아오는 페이지이기도 하다.
##### ![image](https://user-images.githubusercontent.com/80879131/121852455-79294380-cd2a-11eb-8147-58d8586ac2d0.png)


##### 2. Loading Page : Player가 마음의 준비를 하기 위해 약 3초의 시간을 주는 페이지다.
##### ![image](https://user-images.githubusercontent.com/80879131/121852493-847c6f00-cd2a-11eb-84b2-cadbd6062479.png)


##### 3. Game Page : 게임은 1,2,3 단계로 이루어지며, Player는 왼쪽에 Alien은 오른쪽에 나타난다. 왼쪽 위에는 Player의 생명, 오른쪽 위에는 Level, 왼쪽 아래는 Score, 오른쪽 아래에는 Time이 보여진다.
##### ![image](https://user-images.githubusercontent.com/80879131/121852522-90683100-cd2a-11eb-8d34-6f74e0e5ed30.png)


##### 4. Level-up Page : Player가 주어진 시간 안에 목숨을 모두 잃지 않고 Level마다 정해진 Score을 달성하면 level up page가 나온다. 'You win!'이라는 문구와 함께 quit과 next를 고를 수 있게 한다. quit을 누르면 1. start page로 이동하며, next를 누르면 다음 단계로 넘어간다.
##### ![image](https://user-images.githubusercontent.com/80879131/121852545-9bbb5c80-cd2a-11eb-8de8-c070cd0ea5cb.png)


##### 5. Lose Page : Player의 시간이 초과되거나 정해진 Score에 도달하지 못한 경우 나오는 페이지다. 통과 score와 Player의 score를 비교하여 보여준다. quit을 누르면 1. start page로 이동하며, replay를 누르면 해당 단계를 다시 도전하게 된다.
##### ![image](https://user-images.githubusercontent.com/80879131/121852563-a2e26a80-cd2a-11eb-825c-fafe7871ec3b.png)


##### 6. Final Winner Page : replay 버튼을 누르면 Level1부터 시작할 수 있다.
##### ![image](https://user-images.githubusercontent.com/80879131/121852595-ad9cff80-cd2a-11eb-9512-b132ee4b7adf.png)
